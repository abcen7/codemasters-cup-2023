from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, ParseMode

from main import \
    bot, \
    dp

from services import \
    EmployeesService, \
    UsersService

from handlers.constants import \
    EmployeeSearchMessages, \
    SearchType

from handlers.utils import \
    get_result_or_failed, \
    get_employee_card, validate_period_of_time

from keyboards.constants import \
    EmployeeSearchButtons, \
    EmployeeMainButtons

from keyboards.executor import \
    executor_cb, \
    get_search_keyboard, \
    get_main_keyboard, \
    get_employee_card_actions_keyboard, \
    get_job_titles_list_keyboard


class SearchEmployee(StatesGroup):
    search_name_data = State()
    search_surname_data = State()
    search_job_title_data = State()
    search_project_data = State()
    search_patronymic_data = State()
    search_period_of_time_data = State()


@dp.callback_query_handler(executor_cb.filter(action=EmployeeMainButtons.SEARCH_DATA.value))
async def process_search_employee_callback(call: CallbackQuery) -> None:
    await bot.send_message(
        call.from_user.id,
        EmployeeSearchMessages.LIST_COMMANDS.value,
        reply_markup=get_search_keyboard()
    )


@dp.message_handler(commands=["employee_search"])
async def process_search_employee_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        EmployeeSearchMessages.LIST_COMMANDS.value
    )


"""Поиск по имени сотрудника"""


@dp.callback_query_handler(executor_cb.filter(action=EmployeeSearchButtons.NAME_DATA.value))
async def process_search_employee_name_callback(call: CallbackQuery) -> None:
    await bot.send_message(
        call.from_user.id,
        EmployeeSearchMessages.ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_name_data.set()


@dp.message_handler(commands=["search_employee_name"])
async def search_employee_by_name(message: types.Message) -> None:
    await message.answer(
        EmployeeSearchMessages.ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_name_data.set()


@dp.message_handler(state=SearchEmployee.search_name_data)
async def process_search_employee_by_name(message: types.Message, state: FSMContext):
    search_data = message.text
    api_result = await EmployeesService.search(search_data, SearchType.NAME)
    await get_result_or_failed(api_result, message)
    await state.finish()


"""Поиск по фамилии сотрудника"""


@dp.message_handler(commands=["search_employee_surname"])
async def search_employee_by_surname(message: types.Message) -> None:
    await message.answer(
        EmployeeSearchMessages.ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_surname_data.set()


@dp.callback_query_handler(executor_cb.filter(action=EmployeeSearchButtons.SURNAME_DATA.value))
async def process_search_employee_surname_callback(call: CallbackQuery, callback_data) -> None:
    await bot.send_message(
        call.from_user.id,
        EmployeeSearchMessages.ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_surname_data.set()


@dp.message_handler(state=SearchEmployee.search_surname_data)
async def process_search_employee_by_surname(message: types.Message, state: FSMContext):
    search_data = message.text
    api_result = await EmployeesService.search(search_data, SearchType.SURNAME)
    await get_result_or_failed(api_result, message)
    await state.finish()


"""Поиск по должности сотрудника"""


@dp.callback_query_handler(executor_cb.filter(action=EmployeeSearchButtons.JOB_TITLE_DATA.value))
async def process_search_employee_job_title_callback(call: CallbackQuery) -> None:
    await bot.send_message(
        call.from_user.id,
        EmployeeSearchMessages.LIST_JOB_TITLES.value,
        reply_markup=await get_job_titles_list_keyboard()
    )


@dp.message_handler(commands=["search_employee_job_title"])
async def search_employee_by_job_title(message: types.Message) -> None:
    await message.answer(
        EmployeeSearchMessages.LIST_JOB_TITLES.value,
        reply_markup=await get_job_titles_list_keyboard()
    )


@dp.callback_query_handler(lambda c: c.data.startswith('employees_job_title_info_'))
async def process_search_employee_job_title_callback(call: CallbackQuery) -> None:
    employee_job_title = call.data.replace('employees_job_title_info_', '')
    api_result = await EmployeesService.search(employee_job_title, SearchType.JOB_TITLE)
    await get_result_or_failed(api_result, call.message)


"""Поиск по проекту сотрудника"""


@dp.message_handler(commands=["search_employee_project"])
async def search_employee_by_project(message: types.Message) -> None:
    await message.answer(
        EmployeeSearchMessages.ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_project_data.set()


@dp.callback_query_handler(executor_cb.filter(action=EmployeeSearchButtons.PROJECT_DATA.value))
async def process_search_employee_project_callback(call: CallbackQuery) -> None:
    await bot.send_message(
        call.from_user.id,
        EmployeeSearchMessages.ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_project_data.set()


@dp.message_handler(state=SearchEmployee.search_project_data)
async def process_search_employee_by_project(message: types.Message, state: FSMContext):
    search_data = message.text
    api_result = await EmployeesService.search(search_data, SearchType.PROJECT)
    await get_result_or_failed(api_result, message)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('employee_info_'))
async def process_view_employee_card(callback_data: CallbackQuery) -> None:
    employee_id = callback_data.data.replace('employee_info_', '')
    employee_from_api = await EmployeesService.get_one(employee_id)
    keyboard = None
    if await UsersService.is_user_admin(callback_data.from_user.id):
        keyboard = get_employee_card_actions_keyboard(employee_id)
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text=await get_employee_card(employee_from_api),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
        reply_markup=keyboard
    )


"""Поиск по отчеству"""


@dp.message_handler(commands=["search_employee_patronymic"])
async def search_employee_by_patronymic(message: types.Message) -> None:
    await message.answer(
        EmployeeSearchMessages.ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_patronymic_data.set()


@dp.callback_query_handler(executor_cb.filter(action=EmployeeSearchButtons.PATRONYMIC_DATA.value))
async def process_search_employee_patronymic_callback(call: CallbackQuery, callback_data) -> None:
    await bot.send_message(
        call.from_user.id,
        EmployeeSearchMessages.ASK.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_patronymic_data.set()


@dp.message_handler(state=SearchEmployee.search_patronymic_data)
async def process_search_employee_by_patronymic(message: types.Message, state: FSMContext):
    search_data = message.text
    api_result = await EmployeesService.search(search_data, SearchType.PATRONYMIC)
    await get_result_or_failed(api_result, message)
    await state.finish()


"""Поиск по периоду времени работы"""


@dp.message_handler(commands=["search_employee_time"])
async def search_employee_by_period_of_time(message: types.Message) -> None:
    await message.answer(
        EmployeeSearchMessages.ASK_PERIOD_OF_TIME.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_period_of_time_data.set()


@dp.callback_query_handler(executor_cb.filter(action=EmployeeSearchButtons.PERIOD_OF_TIME_DATA.value))
async def process_search_employee_period_of_time_callback(call: CallbackQuery, callback_data) -> None:
    await bot.send_message(
        call.from_user.id,
        EmployeeSearchMessages.ASK_PERIOD_OF_TIME.value,
        reply_markup=get_main_keyboard()
    )
    await SearchEmployee.search_period_of_time_data.set()


@dp.message_handler(state=SearchEmployee.search_period_of_time_data)
async def process_search_employee_by_period_of_time(message: types.Message, state: FSMContext):
    search_data = message.text
    result = await validate_period_of_time(search_data)
    if not result:
        await bot.send_message(
            message.from_user.id,
            EmployeeSearchMessages.FAILED.value,
            reply_markup=get_main_keyboard()
        )
    else:
        print(result)
        api_result = await EmployeesService.search(result, SearchType.PERIOD_OF_TIME)
        await get_result_or_failed(api_result, message)
    await state.finish()
