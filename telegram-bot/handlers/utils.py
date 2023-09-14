import datetime
from typing import Dict, List, NoReturn

from aiogram import types
from aiogram.types import ParseMode

from handlers.constants import SearchResultMessages, API_TO_RESULT, NEW_LINE, AVATAR_PATH, CREATED, ID
from services import EmployeesService


async def get_result_or_failed(
        employees: List[Dict[str, str]],
        message: types.Message,
) -> NoReturn:
    print(employees)
    if not employees or len(employees) == 0:
        await message.answer(
            SearchResultMessages.SEARCH_RESULT_NOT_FOUND.value,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False
        )
    else:
        for employee in employees[:5]:
            employee_card = []
            for key in employee:
                if key == ID:
                    employee_card.append(f'<b>ID: </b><pre>{employee[key]}</pre>')
                if key == AVATAR_PATH:
                    avatar_file = await EmployeesService.get_file(employee[key])
                    employee_card.append(f'<a href="{avatar_file}">&#8205;</a>')
                if key == CREATED:
                    employee_card.append(f'<b>Дата прихода</b>: {datetime.datetime.fromtimestamp(employee[key])}')
                if key in API_TO_RESULT and employee[key] is not None:
                    employee_card.append(str(API_TO_RESULT[key]) + str(employee[key]))
            await message.answer(
                NEW_LINE.join(employee_card),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False
            )
