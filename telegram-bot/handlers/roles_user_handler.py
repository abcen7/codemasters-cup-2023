from handlers.constants import UserRolesMessages, UserRoles
from keyboards.executor import get_main_keyboard
from main import dp
from services.users import UsersService
from aiogram import types


@dp.message_handler(commands=["user"])
async def change_role_to_user(message: types.Message) -> None:
    user_id = message.from_user.id
    await UsersService.change_role(user_id, UserRoles.USER.value)
    await message.answer(
        UserRolesMessages.CHANGED.value,
        reply_markup=get_main_keyboard()
    )


@dp.message_handler(commands=["admin"])
async def change_role_to_admin(message: types.Message) -> None:
    user_id = message.from_user.id
    await UsersService.change_role(user_id, UserRoles.ADMIN.value)
    await message.answer(
        UserRolesMessages.CHANGED.value,
        reply_markup=get_main_keyboard()
    )
