from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from handlers import EmployeeAskDataMessages
from handlers.constants import EmployeeDeleteMessages, EmployeeUpdateMessages
from keyboards.constants import EMPLOYEE_REMOVE_DATA, STOP_FILLING
from keyboards.executor import executor_cb, get_stop_filling_keyboard, get_main_keyboard
from main import dp, bot
from services import EmployeesService


class DeleteEmployee(StatesGroup):
    id = State()
    is_verified = State()


@dp.callback_query_handler(executor_cb.filter(action=EMPLOYEE_REMOVE_DATA))
async def process_delete_employee_callback(call: CallbackQuery, callback_data) -> None:
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
    await message.answer(
        EmployeeDeleteMessages.DELETE.value
    )
    await message.answer(
        EmployeeAskDataMessages.ID.value,
        reply_markup=get_stop_filling_keyboard()
    )
    await DeleteEmployee.id.set()


@dp.message_handler(lambda message: message.text == STOP_FILLING, state="*")
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
    solution = message.text.lower() == "да"
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
