from .models import User
from .repositories import UsersRepository


class UsersService:
    object_model = User

    def __init__(self) -> None:
        self.repository = UsersRepository()

    async def create(self, create_object: object_model) -> object_model:
        return await self.repository.create(dict(create_object))
