from bson import ObjectId
from pymongo import ReturnDocument

from .models import User
from database import Users

from .dependencies import is_document_found


class UsersRepository:
    object_model = User

    def __init__(self) -> None:
        self.collection = Users

    async def is_user_exist(self, telegram_id: int) -> object_model:
        return (await self.collection.find_one({"telegram_id": telegram_id})) is not None

    async def get_by_telegram_id(self, telegram_id: int) -> object_model:
        return await is_document_found(
            await self.collection.find_one(
                {"telegram_id": telegram_id},
            )
        )

    async def create(self, object_create: dict) -> object_model:
        await self.collection.insert_one(object_create)
        return self.object_model.model_validate(object_create)

    async def update(self, telegram_id: int, object_update: dict) -> object_model:
        return await is_document_found(
            await self.collection.find_one_and_update(
                {"telegram_id": telegram_id},
                {"$set": object_update},
                return_document=ReturnDocument.AFTER,
            )
        )
