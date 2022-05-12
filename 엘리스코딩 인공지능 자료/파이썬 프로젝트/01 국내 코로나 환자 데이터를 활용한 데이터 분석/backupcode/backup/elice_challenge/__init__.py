import getpass
from typing import Optional

from .exercise import ExerciseHandler, ExerciseException

_exercise_handler = None


async def _init_exercise_handler() -> bool:
    global _exercise_handler

    email = input('이메일 > ')
    password = getpass.getpass('비밀번호 > ')

    _exercise_handler = ExerciseHandler(email=email, password=password)

    try:
        await _exercise_handler.refresh_sessionkey()
    except Exception:
        print('비밀번호가 일치하지 않습니다.')
        await _exercise_handler.close()
        _exercise_handler = None
        return False

    return True


async def upload(*, is_close_session: Optional[bool] = False) -> None:
    if _exercise_handler is None:
        if not (await _init_exercise_handler()):
            return

    assert _exercise_handler is not None

    try:
        await _exercise_handler.upload()
    except ExerciseException as ex:
        print(str(ex))
    except Exception as ex:
        print('관리자에게 문의해주세요. (%s)' % str(ex))
    else:
        print('업로드가 완료되었습니다.')
    finally:
        if is_close_session:
            await _exercise_handler.close()


async def check_score(*, is_close_session: Optional[bool] = False):
    if _exercise_handler is None:
        if not (await _init_exercise_handler()):
            return

    assert _exercise_handler is not None

    try:
        await _exercise_handler.submit()
    except ExerciseException as ex:
        print(str(ex))
    except Exception as ex:
        print('관리자에게 문의해주세요. (%s)' % str(ex))
    else:
        score = _exercise_handler.get_score()

        if score is None:
            print('점수가 확인되지 않습니다.')
        else:
            print('점수는 %d 점 입니다.' % score)

    finally:
        if is_close_session:
            await _exercise_handler.close()
