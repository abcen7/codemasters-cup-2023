from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, ParseMode

from handlers.constants import UserSearchMessages, EmployeeCreateMessages, SearchType
from handlers.fill_employee_handler import FillEmployee
from handlers.utils import get_result_or_failed
from keyboards.constants import EMPLOYEE_SEARCH_DATA
from keyboards.executor import executor_cb, get_search_keyboard, get_main_keyboard
from main import bot, dp
from services import EmployeesService


class SearchEmployee(StatesGroup):
    search_name_data = State()
    search_surname_data = State()
    search_job_title_data = State()
    search_project_data = State()


@dp.callback_query_handler(executor_cb.filter(action=EMPLOYEE_SEARCH_DATA))
async def process_search_employee_callback(call: CallbackQuery, callback_data) -> None:
    await bot.send_message(
        call.from_user.id,
        UserSearchMessages.LIST_SEARCH_COMMANDS.value
    )


@dp.message_handler(commands=["search_employee_name"])
async def search_employee_by_name(message: types.Message) -> None:
    """
    Поиск по имени сотрудника
    """
    await message.answer(
        UserSearchMessages.USER_SEARCH_ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_name_data.set()


@dp.message_handler(state=SearchEmployee.search_name_data)
async def process_search_employee_by_name(message: types.Message, state: FSMContext):
    search_data = message.text
    api_result = await EmployeesService.search(search_data, SearchType.NAME)
    await get_result_or_failed(api_result, message)
    await state.finish()


@dp.message_handler(commands=["search_employee_surname"])
async def search_employee_by_surname(message: types.Message) -> None:
    """
    Поиск по фамилии сотрудника
    """
    await message.answer(
        UserSearchMessages.USER_SEARCH_ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_surname_data.set()


@dp.message_handler(state=SearchEmployee.search_surname_data)
async def process_search_employee_by_surname(message: types.Message, state: FSMContext):
    search_data = message.text
    api_result = await EmployeesService.search(search_data, SearchType.SURNAME)
    await get_result_or_failed(api_result, message)
    await state.finish()


@dp.message_handler(commands=["search_employee_job_title"])
async def search_employee_by_job_title(message: types.Message) -> None:
    """
    Поиск по должности сотрудника
    """
    await message.answer(
        UserSearchMessages.USER_SEARCH_ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_job_title_data.set()


@dp.message_handler(state=SearchEmployee.search_job_title_data)
async def process_search_employee_by_job_title(message: types.Message, state: FSMContext):
    search_data = message.text
    api_result = await EmployeesService.search(search_data, SearchType.JOB_TITLE)
    await get_result_or_failed(api_result, message)
    await state.finish()


@dp.message_handler(commands=["search_employee_project"])
async def search_employee_by_project(message: types.Message) -> None:
    """
    Поиск по проекту сотрудника
    """
    await message.answer(
        UserSearchMessages.USER_SEARCH_ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_project_data.set()


@dp.message_handler(state=SearchEmployee.search_project_data)
async def process_search_employee_by_project(message: types.Message, state: FSMContext):
    search_data = message.text
    api_result = await EmployeesService.search(search_data, SearchType.PROJECT)
    await get_result_or_failed(api_result, message)
    await state.finish()
