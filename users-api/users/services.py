from .exceptions import UserIsAlreadyExist
from .models import User
from .repositories import UsersRepository
from .schemas import UpdateUser


class UsersService:
    object_model = User

    def __init__(self) -> None:
        self.repository = UsersRepository()

    async def create(self, create_object: object_model) -> object_model:
        if await self.repository.is_user_exist(create_object.telegram_id):
            raise UserIsAlreadyExist
        return await self.repository.create(dict(create_object))

    async def get_one(self, telegram_id: int) -> object_model:
        return await self.repository.get_by_telegram_id(telegram_id)

    async def update(self, telegram_id: int, params_for_update: UpdateUser) -> object_model:
        return await self.repository.update(
            telegram_id,
            params_for_update.model_dump(exclude_none=True)
        )
