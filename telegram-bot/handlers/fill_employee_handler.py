from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from config import TEMP_STATIC_PATH
from .utils import generate_unique_filename
from main import bot, dp
from services import \
    EmployeesService, \
    UsersService

from handlers.constants import \
    EmployeeCreateMessages, \
    EmployeeAskDataMessages, \
    UserRolesMessages

from keyboards.executor import \
    executor_cb, \
    get_optional_field_keyboard, \
    get_stop_filling_keyboard, \
    get_main_keyboard

from keyboards.constants import \
    STOP_FILLING_FIELD, \
    OPTIONAL_FIELD, \
    EmployeeMainButtons


class FillEmployee(StatesGroup):
    name = State()
    patronymic = State()
    surname = State()
    job_title = State()
    project = State()
    avatar_path = State()


@dp.callback_query_handler(executor_cb.filter(action=EmployeeMainButtons.ADD_DATA.value))
async def process_add_user_callback(call: CallbackQuery) -> None:
    if not await UsersService.is_user_admin(call.from_user.id):
        await call.answer(
            UserRolesMessages.NOT_PERMITTED.value
        )
        return
    await bot.send_message(
        call.from_user.id,
        EmployeeCreateMessages.CREATE.value
    )
    await bot.send_message(
        call.from_user.id,
        EmployeeAskDataMessages.NAME.value,
        reply_markup=get_stop_filling_keyboard()
    )
    await FillEmployee.name.set()


@dp.message_handler(commands=["employee_add"])
async def process_add_user_command(message: types.Message):
    if not await UsersService.is_user_admin(message.from_user.id):
        await message.answer(
            UserRolesMessages.NOT_PERMITTED.value
        )
        return
    await message.answer(
        EmployeeCreateMessages.CREATE.value
    )
    await message.answer(
        EmployeeAskDataMessages.NAME.value,
        reply_markup=get_stop_filling_keyboard()
    )
    await FillEmployee.name.set()


@dp.message_handler(lambda message: message.text == STOP_FILLING_FIELD, state="*")
async def stop_filling(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        EmployeeCreateMessages.STOPPED.value,
        reply_markup=get_main_keyboard()
    )


@dp.message_handler(state=FillEmployee.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(
        EmployeeAskDataMessages.PATRONYMIC.value,
        reply_markup=get_optional_field_keyboard()
    )
    await FillEmployee.next()


@dp.message_handler(state=FillEmployee.patronymic)
async def process_patronymic(message: types.Message, state: FSMContext):
    patronymic = message.text
    await state.update_data(patronymic=patronymic)
    await message.answer(
        EmployeeAskDataMessages.SURNAME.value,
        reply_markup=get_stop_filling_keyboard()
    )
    await FillEmployee.next()


@dp.message_handler(state=FillEmployee.surname)
async def process_surname(message: types.Message, state: FSMContext):
    surname = message.text
    await state.update_data(surname=surname)
    await message.answer(EmployeeAskDataMessages.JOB_TITLE.value)
    await FillEmployee.next()


@dp.message_handler(state=FillEmployee.job_title)
async def process_job_title(message: types.Message, state: FSMContext):
    job_title = message.text
    await state.update_data(job_title=job_title)
    await message.answer(EmployeeAskDataMessages.PROJECT.value)
    await FillEmployee.next()


@dp.message_handler(state=FillEmployee.project)
async def process_project(message: types.Message, state: FSMContext):
    project = message.text
    await state.update_data(project=project)
    await message.answer(
        EmployeeAskDataMessages.AVATAR.value,
        reply_markup=get_optional_field_keyboard()
    )
    await FillEmployee.next()


@dp.message_handler(state=FillEmployee.avatar_path, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_avatar(message: types.Message, state: FSMContext):
    if message.content_type == str(types.ContentType.PHOTO):
        photo = message.photo[-1]
        file_id = photo.file_id
        filename = await generate_unique_filename()
        full_file_path = Path(TEMP_STATIC_PATH) / filename
        await bot.download_file_by_id(file_id, full_file_path)
        await state.update_data(avatar_path=full_file_path)
    else:
        await state.update_data(avatar_path=OPTIONAL_FIELD)
    await message.answer(
        EmployeeCreateMessages.SUCCESS.value,
        reply_markup=get_main_keyboard()
    )
    await EmployeesService.new(state)
    await state.finish()
