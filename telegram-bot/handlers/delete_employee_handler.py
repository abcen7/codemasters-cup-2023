from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from handlers import EmployeeAskDataMessages

from main import \
    dp, \
    bot

from services import \
    EmployeesService, \
    UsersService

from handlers.constants import \
    EmployeeDeleteMessages, \
    EmployeeUpdateMessages, \
    DELETE_VERIFIED_YES, \
    UserRolesMessages

from keyboards.constants import \
    STOP_FILLING_FIELD, \
    EmployeeCardActionsButtons, \
    EmployeeMainButtons

from keyboards.executor import \
    executor_cb, \
    get_stop_filling_keyboard, \
    get_main_keyboard, \
    employee_cb


class DeleteEmployee(StatesGroup):
    id = State()
    is_verified = State()


# DeleteEmployee from search keyboard handler
@dp.callback_query_handler(employee_cb.filter(action=EmployeeCardActionsButtons.DELETE_DATA.value))
async def process_delete_employee_inline_callback(call: CallbackQuery, callback_data, state: FSMContext) -> None:
    if not await UsersService.is_user_admin(call.from_user.id):
        await call.answer(
            UserRolesMessages.NOT_PERMITTED.value
        )
        return
    await bot.send_message(
        call.from_user.id,
        EmployeeDeleteMessages.DELETE.value
    )
    employee_id = callback_data["employee_id"]
    if await EmployeesService.is_employee_exist(employee_id):
        await state.update_data(id=employee_id)
        await bot.send_message(
            call.from_user.id,
            EmployeeDeleteMessages.IS_VERIFIED.value,
            reply_markup=get_stop_filling_keyboard()
        )
        await DeleteEmployee.is_verified.set()
    else:
        await call.answer(
            call.from_user.id,
            EmployeeDeleteMessages.INVALID_ID.value
        )


@dp.callback_query_handler(executor_cb.filter(action=EmployeeMainButtons.DELETE_DATA.value))
async def process_delete_employee_callback(call: CallbackQuery, callback_data) -> None:
    if not await UsersService.is_user_admin(call.from_user.id):
        await call.answer(
            UserRolesMessages.NOT_PERMITTED.value
        )
        return
    await bot.send_message(
        call.from_user.id,
        EmployeeDeleteMessages.DELETE.value
    )
    await bot.send_message(
        call.from_user.id,
        EmployeeAskDataMessages.ID.value,
        reply_markup=get_stop_filling_keyboard()
    )
    await DeleteEmployee.id.set()


@dp.message_handler(commands=["employee_delete"])
async def process_delete_employee_command(message: types.Message):
    if not await UsersService.is_user_admin(message.from_user.id):
        await message.answer(
            UserRolesMessages.NOT_PERMITTED.value
        )
        return
    await message.answer(
        EmployeeDeleteMessages.DELETE.value
    )
    await message.answer(
        EmployeeAskDataMessages.ID.value,
        reply_markup=get_stop_filling_keyboard()
    )
    await DeleteEmployee.id.set()


@dp.message_handler(lambda message: message.text == STOP_FILLING_FIELD, state="*")
async def stop_filling(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        EmployeeUpdateMessages.STOPPED.value,
        reply_markup=get_main_keyboard()
    )


@dp.message_handler(state=DeleteEmployee.id)
async def process_id(message: types.Message, state: FSMContext):
    employee_id = message.text
    if await EmployeesService.is_employee_exist(employee_id):
        await state.update_data(id=employee_id)
        await message.answer(
            EmployeeDeleteMessages.IS_VERIFIED.value,
            reply_markup=get_stop_filling_keyboard()
        )
        await DeleteEmployee.next()
    else:
        await message.answer(
            EmployeeDeleteMessages.INVALID_ID.value
        )


@dp.message_handler(state=DeleteEmployee.is_verified)
async def process_delete_employee(message: types.Message, state: FSMContext):
    solution = message.text.lower() == DELETE_VERIFIED_YES
    if solution:
        await state.update_data(is_verified=True)
        await message.answer(
            EmployeeDeleteMessages.SUCCESS.value,
            reply_markup=get_main_keyboard()
        )
        state_data = await state.get_data()
        await EmployeesService.delete(state_data['id'])
        await state.finish()
    else:
        await message.answer(
            EmployeeDeleteMessages.CANCEL.value,
            reply_markup=get_main_keyboard()
        )
