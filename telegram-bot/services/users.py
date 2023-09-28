from typing import NoReturn, Dict

from aiohttp import \
    ClientSession, \
    ClientError, \
    TCPConnector

from config import API_URL
from handlers.constants import UserRoles


class UsersService:
    API_USERS = API_URL + '/users'

    @staticmethod
    async def new(telegram_id: int) -> NoReturn:
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.post(UsersService.API_USERS, json={
                    "telegram_id": telegram_id
                }) as response:
                    response.raise_for_status()
            except ClientError as err:
                print(f"User is already exists... {err}")

    @staticmethod
    async def get_by_telegram_id(telegram_id: int) -> Dict:
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.get(UsersService.API_USERS + f'/{telegram_id}') as response:
                    return await response.json()
            except ClientError as err:
                print(f"Can't change the role {err}")

    @staticmethod
    async def change_role(telegram_id: int, role: str) -> NoReturn:
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.patch(UsersService.API_USERS + f'/{telegram_id}', json={
                    "is_admin": role == UserRoles.ADMIN.value
                }) as response:
                    response.raise_for_status()
            except ClientError as err:
                print(f"Can't change the role {err}")

    @staticmethod
    async def is_user_admin(telegram_id: int) -> bool:
        user = await UsersService.get_by_telegram_id(telegram_id)
        return user['is_admin']
