from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from .models import User
from database import Users

from .dependencies import is_document_found
from base import BaseRepository


class UsersRepository(BaseRepository):
    object_model = User

    def __init__(self):
        super().__init__(Users)

    async def create(self, object_create: dict) -> object_model:
        await self.collection.insert_one(object_create)
        return self.object_model.model_validate(object_create)
