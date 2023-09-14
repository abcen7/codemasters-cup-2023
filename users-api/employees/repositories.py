from typing import List, Dict
from bson import ObjectId

from database import Employees
from .models import Employee

from .dependencies import is_document_found
from pymongo import ReturnDocument


class EmployeesRepository:
    object_model = Employee

    def __init__(self) -> None:
        self.collection = Employees

    async def find_many_within_search(self, params_for_search: List[Dict[str, Dict[str, str]]]) -> List[object_model]:
        return [document async for document in self.collection.find({"$and": params_for_search})]

    async def get_all(self, limit=20) -> List[object_model]:
        return [document async for document in self.collection.find({}).limit(limit)]

    async def get_by_id(self, object_id: str) -> object_model:
        return await is_document_found(
            await self.collection.find_one({"_id": ObjectId(object_id)})
        )

    async def update(self, employee_id: str, object_update: dict) -> object_model:
        return await is_document_found(
            await self.collection.find_one_and_update(
                {"_id": ObjectId(employee_id)},
                {"$set": object_update},
                return_document=ReturnDocument.AFTER,
            )
        )

    async def create(self, object_create: Dict) -> object_model:
        await self.collection.insert_one(object_create)
        return self.object_model.model_validate(object_create)

    async def delete(self, object_id: str) -> object_model:
        return await is_document_found(
            await self.collection.find_one_and_delete({"_id": ObjectId(object_id)})
        )
