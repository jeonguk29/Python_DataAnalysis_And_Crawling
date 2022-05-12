import asyncio
import json
import time
import os
from typing import List, NamedTuple, Optional

from aiohttp import WSMsgType

from .config import (API_WS_SERVER, MATERIAL_EXERCISE_ID,
                     MAX_TOTAL_FILE_SIZE_BYTES, ORG_NAME_SHORT, ROOM_PERPARED_TIMEOUT,
                     RUNNING_TIMEOUT, UPLOAD_FILENAME_LIST)
from .utils.elice_api import EliceAPIHandler, EliceAPIException


class _RoomInfo(NamedTuple):
    exercise_room_id: int
    exercise_image_id: int
    room_token: str


class ExerciseException(Exception):
    pass


class ExerciseHandler(EliceAPIHandler):
    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)

        self._running_id: Optional[str] = None
        self._running_score: Optional[int] = None
        self._forwarder_ws_uri: Optional[str] = None
        self._stop_event = asyncio.Event()

    def get_score(self) -> Optional[int]:
        return self._running_score

    def _init_running(self) -> None:
        self._running_score = None
        self._running_id = None
        self._forwarder_ws_uri = None
        self._stop_event.clear()

    async def upload(self) -> None:
        try:
            room_info = await self._get_room_info()

            await self._add_user_file(room_info.exercise_room_id)
        except EliceAPIException as ex:
            raise ExerciseException(str(ex))

    async def submit(self) -> None:
        self._init_running()

        runner_room_task: Optional[asyncio.Future] = None
        forwarder_task: Optional[asyncio.Future] = None

        try:
            room_info = await self._get_room_info()

            runner_room_task = asyncio.ensure_future(self._runner_room_handler(room_info.room_token))

            start_time = time.monotonic()

            while (not self._stop_event.is_set()
                   and time.monotonic() - start_time < ROOM_PERPARED_TIMEOUT):
                if self._forwarder_ws_uri is not None:
                    break
                await asyncio.sleep(1.0)
            else:
                raise ExerciseException('실습방에 연결할수 없습니다.')

            forwarder_task = asyncio.ensure_future(self._fowarder_handler(room_info.room_token))

            running_response = await self.request(
                'POST',
                f'/org/{ORG_NAME_SHORT}/material_exercise/exercise_running/submit/',
                data={
                    'room_token': room_info.room_token,
                    'run_type': 10,  # Grade
                    'exercise_image_id': room_info.exercise_image_id
                }
            )

            self._running_id = running_response['exercise_running_id']

            while (not self._stop_event.is_set()
                   and time.monotonic() - start_time < RUNNING_TIMEOUT):
                if self._running_score is not None:
                    break
                await asyncio.sleep(1.0)
            else:
                if self._stop_event.is_set():
                    raise ExerciseException('실행도중 에러가 발생했습니다.')
                else:
                    raise ExerciseException('점수 확인 시간(%s 초) 이 지났습니다.' % RUNNING_TIMEOUT)

        except EliceAPIException as ex:
            raise ExerciseException(str(ex))
        finally:
            if runner_room_task is not None:
                runner_room_task.cancel()
                try:
                    await asyncio.wait_for(runner_room_task, timeout=15)
                except asyncio.CancelledError:
                    pass

            if forwarder_task is not None:
                forwarder_task.cancel()
                try:
                    await asyncio.wait_for(forwarder_task, timeout=15)
                except asyncio.CancelledError:
                    pass

    async def _runner_room_handler(self, room_token: str) -> None:
        async with self._session.ws_connect(
                '%s/runner_room/%s' % (API_WS_SERVER, room_token)) as elice_ws:

            async for ws_msg in elice_ws:
                if ws_msg.type != WSMsgType.TEXT:
                    continue

                try:
                    msg_json = json.loads(ws_msg.data)
                except ValueError:
                    await elice_ws.close(message=b'invalid_json')
                    break

                if msg_json['type'] == 'ROOM_PREPARED':
                    self._forwarder_ws_uri = msg_json['data']['forwarder']['ws_uri']

                elif msg_json['type'] == 'EXECUTE_DONE':
                    running_response = await self.request(
                        'GET',
                        f'/org/{ORG_NAME_SHORT}/material_exercise/exercise_running/result/get/',
                        params={'exercise_running_id': self._running_id}
                    )

                    self._running_score = running_response['result']['score']

                elif msg_json['type'] == 'EXECUTE_FAIL_TO_RUN':
                    self._stop_event.set()

    async def _fowarder_handler(self, room_token: str) -> None:
        async with self._session.ws_connect(
                '%s/client/stdio/%s' % (self._forwarder_ws_uri, room_token)) as elice_ws:

            async for ws_msg in elice_ws:
                if ws_msg.type != WSMsgType.TEXT:
                    continue

                try:
                    msg_json = json.loads(ws_msg.data)
                except ValueError:
                    await elice_ws.close(message=b'invalid_json')
                    break

                if msg_json['type'] == 'grader':
                    print(msg_json['data'])

    async def _get_room_info(self) -> _RoomInfo:
        exercise_response = await self.request(
            'GET',
            f'/org/{ORG_NAME_SHORT}/material_exercise/get/',
            params={'material_exercise_id': MATERIAL_EXERCISE_ID}
        )

        exercise_image_id = exercise_response['material_exercise']['ready_exercise_image']['id']

        for exercise_room_json in exercise_response['material_exercise']['exercise_rooms']:
            if exercise_room_json['is_default_room']:
                exercise_room_id = exercise_room_json['id']
                break
        else:
            room_response = await self.request(
                'GET',
                f'/org/{ORG_NAME_SHORT}/material_exercise/default_room/get/',
                params={'material_exercise_id': MATERIAL_EXERCISE_ID}
            )

            exercise_room_id = room_response['exercise_room_id']

        join_response = await self.request(
            'POST',
            f'/org/{ORG_NAME_SHORT}/runner_room/exercise_room/join/',
            data={'exercise_room_id': exercise_room_id}
        )

        room_token = join_response['room_token']

        return _RoomInfo(
            exercise_room_id=exercise_room_id,
            exercise_image_id=exercise_image_id,
            room_token=room_token
        )

    async def _add_user_file(self, exercise_room_id: int) -> None:
        room_response = await self.request(
            'GET',
            f'/org/{ORG_NAME_SHORT}/material_exercise/exercise_room/get/',
            params={'exercise_room_id': exercise_room_id}
        )

        filelist = room_response['exercise_room']['filelist']

        print('이전에 업로드 된 파일 삭제중...')

        for file_name in filelist:
            await self.request(
                'POST',
                f'/org/{ORG_NAME_SHORT}/material_exercise/exercise_room/user_file/delete/',
                data={
                    'exercise_room_id': exercise_room_id,
                    'filename': file_name
                }
            )

        self._check_file_name(UPLOAD_FILENAME_LIST)

        for file_name in UPLOAD_FILENAME_LIST:
            with open(file_name, 'rb') as f:
                await self.request(
                    'POST',
                    f'/org/{ORG_NAME_SHORT}/material_exercise/exercise_room/user_file/add/',
                    data={
                        'exercise_room_id': str(exercise_room_id),
                        'is_task': 'true',
                        'path': '',
                        'user_file': f
                    },
                )

    def _check_file_name(self, file_name_list: List[str]) -> None:
        if not file_name_list:
            raise ExerciseException('파일 경로을 하나 이상 입력하셔야 합니다.')

        total_size = 0
        for file_name in file_name_list:
            try:
                total_size += os.path.getsize(file_name)
            except Exception:
                raise ExerciseException('%s를 찾을 수 없습니다. 파일은 Jupyter tree의 루트에 있어야 합니다.' % file_name)

        if total_size > MAX_TOTAL_FILE_SIZE_BYTES:
            raise ExerciseException('업로드할 파일 크기가 %d bytes 가 넘습니다.' % MAX_TOTAL_FILE_SIZE_BYTES)
