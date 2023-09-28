import os
from typing import List, Dict, NoReturn, Union

import aiohttp
from aiogram.dispatcher import FSMContext
from aiohttp import ClientSession, ClientError, FormData

from config import API_URL
from handlers.constants import SearchType
from keyboards.constants import OPTIONAL_FIELD, DONT_UPDATE_FIELD


class EmployeesService:
    API_EMPLOYEES = API_URL + '/employees'
    API_UPLOAD_FILE = API_URL + '/upload_file'
    AVATAR_PATH = 'avatar_path'
    API_SEARCH = API_URL + '/search/employees'
    API_SEARCH_TIME = API_URL + '/search/employees/time'
    API_GET_FILE = API_URL + '/file'

    LIMIT_EMPLOYEES_SEARCH = 20

    @staticmethod
    async def _prepare_employee_for_create(data: Dict[str, str]) -> Dict[str, str]:
        result = {}
        for key in data:
            if data[key] != OPTIONAL_FIELD:
                result[key] = data[key]

        if EmployeesService.AVATAR_PATH in result:
            result[EmployeesService.AVATAR_PATH] = await EmployeesService._upload_file(
                str(result[EmployeesService.AVATAR_PATH]))

        return result

    @staticmethod
    async def _prepare_employee_for_update(data: Dict[str, str]) -> Dict[str, str]:
        result = {}
        for key in data:
            if data[key] != DONT_UPDATE_FIELD:
                if data[key] != OPTIONAL_FIELD:
                    result[key] = data[key]
                else:
                    result[key] = ""
        if EmployeesService.AVATAR_PATH in result and result[EmployeesService.AVATAR_PATH]:
            result[EmployeesService.AVATAR_PATH] = await EmployeesService._upload_file(
                str(
                    result[EmployeesService.AVATAR_PATH]
                )
            )

        return result

    @staticmethod
    async def _upload_file(path_to_file: str) -> str:
        with open(path_to_file, "rb") as file:
            form = FormData()
            form.add_field('file', file, filename=path_to_file, content_type="image/jpeg")

            async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                try:
                    async with session.post(EmployeesService.API_UPLOAD_FILE, data=form) as response:
                        if response.status == 200:
                            response_json = await response.json()
                            os.remove(path_to_file)
                            return response_json['filename']
                        else:
                            print(f"Ошибка загрузки файла: {response.status}")
                except ClientError as err:
                    print(f"An error occurred: {err}")

    @staticmethod
    async def is_employee_exist(employee_id: str) -> bool:
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.get(EmployeesService.API_EMPLOYEES + f'/{employee_id}') as response:
                    response.raise_for_status()
                    if response.status == 200:
                        return True
                    else:
                        return False
            except ClientError as err:
                print(f"An error occurred: {err}")

    @staticmethod
    async def new(state: FSMContext) -> NoReturn:
        employee = await state.get_data()
        prepared_data = await EmployeesService._prepare_employee_for_create(employee)
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.post(EmployeesService.API_EMPLOYEES, json=prepared_data) as response:
                    response.raise_for_status()
            except ClientError as err:
                print(f"An error occurred: {err}")

    @staticmethod
    async def get_all_job_titles() -> List[str]:
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.get(
                        EmployeesService.API_EMPLOYEES + f'/job_titles',
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except ClientError as err:
                print(f"An error occurred: {err}")

    @staticmethod
    async def get_one(employee_id: str) -> Dict[str, str]:
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.get(
                        EmployeesService.API_EMPLOYEES + f'/{employee_id}',
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except ClientError as err:
                print(f"An error occurred: {err}")

    @staticmethod
    async def update(state: FSMContext) -> NoReturn:
        employee = await state.get_data()
        prepared_data = await EmployeesService._prepare_employee_for_update(employee)
        employee_id = prepared_data.pop('id')
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.patch(
                        EmployeesService.API_EMPLOYEES + f'/{employee_id}',
                        json=prepared_data
                ) as response:
                    response.raise_for_status()
                    print(await response.json())
            except ClientError as err:
                print(f"An error occurred: {err}")

    @staticmethod
    async def delete(employee_id: str) -> NoReturn:
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.delete(
                        EmployeesService.API_EMPLOYEES + f'/{employee_id}',
                ) as response:
                    response.raise_for_status()
                    print(await response.json())
            except ClientError as err:
                print(f"An error occurred: {err}")


    @staticmethod
    async def _prepare_data_for_search(search_data: str | tuple, search_type: SearchType) -> tuple:
        data = None
        api_url_search = None
        if search_type == SearchType.PERIOD_OF_TIME:
            print("YES")
            data = {
                "start_time": search_data[0],
                "end_time": search_data[1]
            }
            api_url_search = EmployeesService.API_SEARCH_TIME
        else:
            data = {search_type.value: search_data}
            api_url_search = EmployeesService.API_SEARCH
        return data, api_url_search

    @staticmethod
    async def search(
            search_data: str | tuple,
            search_type: SearchType,
            offset: int = 0
    ) -> List[Dict[str, str]]:
        data, api_url_search = await EmployeesService._prepare_data_for_search(search_data, search_type)
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.post(
                        url=api_url_search,
                        json=data,
                        params={
                            "limit": EmployeesService.LIMIT_EMPLOYEES_SEARCH,
                            "offset": offset
                        }
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except ClientError as err:
                print(f"An error occurred: {err}")

    @staticmethod
    async def get_file(file_name: str) -> str:
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            try:
                async with session.get(EmployeesService.API_GET_FILE + f'/{file_name}') as response:
                    response.raise_for_status()
                    return await response.json()
            except ClientError as err:
                print(f"An error occurred: {err}")
