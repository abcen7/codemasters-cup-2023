import datetime
import uuid
from typing import Dict, List, NoReturn

from aiogram import types
from aiogram.types import ParseMode

import config
from handlers.constants import \
    SearchResultMessages, \
    API_TO_RESULT, \
    NEW_LINE, \
    EmployeeSearchMessages, \
    EmployeeKeysData

from keyboards.executor import get_employees_list_keyboard
from services import EmployeesService


async def get_employee_card(employee: Dict[str, str]) -> str:
    employee_card = []
    for key, value in employee.items():
        match key:
            case EmployeeKeysData.ID.value:
                employee_card.append(f'<b>ID: </b><pre>{employee[key]}</pre>')
            case EmployeeKeysData.CREATED.value:
                employee_card.append(f'<b>Дата прихода</b>: {datetime.datetime.fromtimestamp(value)}')
            case EmployeeKeysData.AVATAR_PATH.value:
                if value:
                    avatar_file = await EmployeesService.get_file(employee[key])
                    if config.LOCAL_DEVELOPMENT:
                        avatar_file = avatar_file.replace('host.docker.internal', 'localhost')
                    employee_card.append(f'<a href="{avatar_file}">&#8205;</a>')
            case _:
                if key in API_TO_RESULT and value:
                    employee_card.append(str(API_TO_RESULT[key]) + str(employee[key]))
    return NEW_LINE.join(employee_card)


async def get_result_or_failed(
        employees: List[Dict[str, str]],
        message: types.Message,
) -> NoReturn:
    if not employees or len(employees) == 0:
        await message.answer(
            SearchResultMessages.SEARCH_RESULT_NOT_FOUND.value,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False
        )
    else:
        await message.answer(
            EmployeeSearchMessages.LIST_EMPLOYEES.value,
            reply_markup=await get_employees_list_keyboard(employees)
        )


async def generate_unique_filename() -> str:
    return f'{str(uuid.uuid4())}.jpg'


async def validate_period_of_time(period: str) -> tuple[int, int] | bool:
    try:
        start_date, end_date = period.split()
        start_date_unix = int(datetime.datetime.strptime(start_date, '%Y-%m-%d-%H-%M').strftime("%s"))
        end_date_unix = int(datetime.datetime.strptime(end_date, '%Y-%m-%d-%H-%M').strftime("%s"))
        return start_date_unix, end_date_unix
    except BaseException:
        return False
