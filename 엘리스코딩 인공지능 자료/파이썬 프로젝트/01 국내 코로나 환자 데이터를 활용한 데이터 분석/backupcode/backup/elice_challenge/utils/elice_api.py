import json
from typing import Any, Dict, Optional

from aiohttp import ClientSession

from ..config import API_SERVER


class EliceAPIException(Exception):
    pass


class EliceAPIHandler:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self._session = ClientSession()
        self._sessionkey: Optional[str] = None

    async def _request(self,
                       method: str,
                       endpoint: str,
                       *,
                       headers: Optional[Dict[str, Any]] = None,
                       data: Optional[Dict[str, Any]] = None,
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response_raw = await self._session.request(
                method,
                f'{API_SERVER}{endpoint}',
                headers=headers,
                data=data,
                params=params,
            )
        except Exception as ex:
            raise EliceAPIException('서버가 응답하지 않습니다. 관리자에게 문의해주세요. (%s)' % str(ex))

        try:
            response_json = await response_raw.json()
        except json.JSONDecodeError:
            raise EliceAPIException('응답이 JSON Format 이 아닙니다.')

        if response_json['_result']['status'] != 'ok':
            if response_json['fail_code'] == 'no_such_account':
                raise EliceAPIException('이메일이 존재하지 않습니다.')

            elif response_json['fail_code'] == 'wrong_password':
                raise EliceAPIException('비밀번호가 일치하지 않습니다.')

            elif response_json['fail_code'] == 'not_accessible_material':
                raise EliceAPIException('실습에 대한 권한이 없습니다.')

            raise EliceAPIException('관리자에게 문의하세요. (endpoint: %s, response: %s)' % (
                endpoint, response_json))

        return response_json

    async def refresh_sessionkey(self) -> None:
        auth_response = await self._request(
            'POST',
            '/global/auth/login/',
            data={
                'email': self.email,
                'password': self.password
            }
        )

        self._sessionkey = auth_response['sessionkey']

    async def request(self,
                      method: str,
                      endpoint: str,
                      data: Optional[Dict[str, Any]] = None,
                      params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self._sessionkey is None:
            await self.refresh_sessionkey()

        return await self._request(
            method,
            endpoint,
            headers={'Authorization': f'Bearer {self._sessionkey}'},
            data=data,
            params=params,
        )

    async def close(self) -> None:
        await self._session.close()
