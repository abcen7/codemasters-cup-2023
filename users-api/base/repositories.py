from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel

from .dependencies import is_document_found


class BaseRepository:
    """
    BaseRepository contains standard methods for all Repositories.
    When inheriting, specify object_model - the main schema of the object, in __init__ specify the collection that
    contains these objects and main schema of the object.
    """

    object_model = BaseModel

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def get_all(self, limit=20) -> List[object_model]:
        return [document async for document in self.collection.find({}).limit(limit)]

    async def get_by_id(self, object_id: str) -> object_model:
        return await is_document_found(
            await self.collection.find_one({"_id": ObjectId(object_id)})
        )

    async def create(self, object_create: dict) -> object_model:
        await self.collection.insert_one(object_create)
        return self.object_model.model_validate(object_create)

    async def delete(self, object_id: str) -> object_model:
        return await is_document_found(
            await self.collection.find_one_and_delete({"_id": ObjectId(object_id)})
        )
