from aiogram import types
from aiogram.dispatcher.filters import Text

from main import dp

from keyboards.executor import \
    get_main_keyboard, \
    get_commands_keyboard

from handlers.constants import \
    WELCOME_MESSAGE, \
    HELP_MESSAGE

from keyboards.constants import \
    COMMANDS_MESSAGE

from services import \
    UsersService


@dp.message_handler(commands=["start"])
async def start_message(message: types.Message) -> None:
    user_id = message.from_user.id
    await UsersService.new(user_id)
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=get_main_keyboard()
    )


@dp.message_handler(commands=["help"])
async def help_message(message: types.Message) -> None:
    await message.answer(
        HELP_MESSAGE,
        reply_markup=get_main_keyboard()
    )


@dp.message_handler(commands=["commands"])
@dp.message_handler(Text(equals=COMMANDS_MESSAGE))
async def process_commands_button(message: types.Message):
    await message.answer(
        "Активный список команд:",
        reply_markup=await get_commands_keyboard(message.from_user.id)
    )