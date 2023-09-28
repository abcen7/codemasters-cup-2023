from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from config import TEMP_STATIC_PATH
from handlers import generate_unique_filename

from main import \
    bot, \
    dp

from services import \
    EmployeesService, \
    UsersService

from handlers.constants import \
    EmployeeAskDataMessages, \
    EmployeeUpdateMessages, \
    UserRolesMessages

from keyboards.executor import \
    executor_cb, \
    get_stop_filling_keyboard, \
    get_main_keyboard, \
    get_dont_update_field_keyboard, \
    get_optional_and_dont_update_keyboard, \
    employee_cb

from keyboards.constants import \
    STOP_FILLING_FIELD, \
    OPTIONAL_FIELD, \
    EmployeeCardActionsButtons, \
    EmployeeMainButtons, DONT_UPDATE_FIELD


class UpdateEmployee(StatesGroup):
    id = State()
    name = State()
    patronymic = State()
    surname = State()
    job_title = State()
    project = State()
    avatar_path = State()


@dp.callback_query_handler(executor_cb.filter(action=EmployeeMainButtons.UPDATE_DATA.value))
async def process_update_employee_callback(call: CallbackQuery) -> None:
    if not await UsersService.is_user_admin(call.from_user.id):
        await call.answer(
            UserRolesMessages.NOT_PERMITTED.value
        )
        return
    await bot.send_message(
        call.from_user.id,
        EmployeeUpdateMessages.UPDATE.value
    )
    await bot.send_message(
        call.from_user.id,
        EmployeeAskDataMessages.ID.value,
        reply_markup=get_stop_filling_keyboard()
    )
    await UpdateEmployee.id.set()


@dp.message_handler(commands=["employee_update"])
async def process_update_employee_command(message: types.Message):
    if not await UsersService.is_user_admin(message.from_user.id):
        await message.answer(
            UserRolesMessages.NOT_PERMITTED.value
        )
        return
    await message.answer(
        EmployeeUpdateMessages.UPDATE.value
    )
    await message.answer(
        EmployeeAskDataMessages.ID.value,
        reply_markup=get_stop_filling_keyboard()
    )
    await UpdateEmployee.id.set()


@dp.message_handler(lambda message: message.text == STOP_FILLING_FIELD, state="*")
async def stop_filling(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        EmployeeUpdateMessages.STOPPED.value,
        reply_markup=get_main_keyboard()
    )


# UpdateEmployee from search keyboard handler
@dp.callback_query_handler(employee_cb.filter(action=EmployeeCardActionsButtons.EDIT_DATA.value))
async def process_update_employee_callback(call: CallbackQuery, callback_data, state: FSMContext) -> None:
    if not await UsersService.is_user_admin(call.from_user.id):
        await call.answer(
            UserRolesMessages.NOT_PERMITTED.value
        )
        return
    await bot.send_message(
        call.from_user.id,
        EmployeeUpdateMessages.UPDATE.value
    )
    employee_id = callback_data["employee_id"]
    if await EmployeesService.is_employee_exist(employee_id):
        await state.update_data(id=employee_id)
        await bot.send_message(
            call.from_user.id,
            EmployeeAskDataMessages.NAME.value,
            reply_markup=get_dont_update_field_keyboard()
        )
        await UpdateEmployee.name.set()
    else:
        await bot.send_message(
            call.from_user.id,
            EmployeeUpdateMessages.INVALID_ID.value
        )


@dp.message_handler(state=UpdateEmployee.id)
async def process_id(message: types.Message, state: FSMContext):
    employee_id = message.text
    # Is employee exist?
    if await EmployeesService.is_employee_exist(employee_id):
        await state.update_data(id=employee_id)
        await message.answer(
            EmployeeAskDataMessages.NAME.value,
            reply_markup=get_dont_update_field_keyboard()
        )
        await UpdateEmployee.next()
    else:
        await message.answer(
            EmployeeUpdateMessages.INVALID_ID.value
        )


@dp.message_handler(state=UpdateEmployee.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(
        EmployeeAskDataMessages.PATRONYMIC.value,
        reply_markup=get_optional_and_dont_update_keyboard()
    )
    await UpdateEmployee.next()


@dp.message_handler(state=UpdateEmployee.patronymic)
async def process_patronymic(message: types.Message, state: FSMContext):
    patronymic = message.text
    await state.update_data(patronymic=patronymic)
    await message.answer(
        EmployeeAskDataMessages.SURNAME.value,
        reply_markup=get_dont_update_field_keyboard()
    )
    await UpdateEmployee.next()


@dp.message_handler(state=UpdateEmployee.surname)
async def process_surname(message: types.Message, state: FSMContext):
    surname = message.text
    await state.update_data(surname=surname)
    await message.answer(EmployeeAskDataMessages.JOB_TITLE.value)
    await UpdateEmployee.next()


@dp.message_handler(state=UpdateEmployee.job_title)
async def process_job_title(message: types.Message, state: FSMContext):
    job_title = message.text
    await state.update_data(job_title=job_title)
    await message.answer(EmployeeAskDataMessages.PROJECT.value)
    await UpdateEmployee.next()


@dp.message_handler(state=UpdateEmployee.project)
async def process_project(message: types.Message, state: FSMContext):
    project = message.text
    await state.update_data(project=project)
    await message.answer(
        EmployeeAskDataMessages.AVATAR.value,
        reply_markup=get_optional_and_dont_update_keyboard()
    )
    await UpdateEmployee.next()


@dp.message_handler(state=UpdateEmployee.avatar_path, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_avatar(message: types.Message, state: FSMContext):
    if message.content_type == str(types.ContentType.PHOTO):
        photo = message.photo[-1]
        file_id = photo.file_id
        filename = await generate_unique_filename()
        full_file_path = Path(TEMP_STATIC_PATH) / filename
        await bot.download_file_by_id(file_id, full_file_path)
        await state.update_data(avatar_path=full_file_path)
    elif message.text == DONT_UPDATE_FIELD or message.text == OPTIONAL_FIELD:
        await state.update_data(avatar_path=message.text)
    else:
        await state.update_data(avatar_path=DONT_UPDATE_FIELD)
    await message.answer(
        EmployeeUpdateMessages.SUCCESS.value,
        reply_markup=get_main_keyboard()
    )
    await EmployeesService.update(state)
    await state.finish()
