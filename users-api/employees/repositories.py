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

    async def get_all_job_titles(self) -> List[str]:
        job_titles = []
        documents = [document async for document in self.collection.find({}, {"job_title": 1, "_id": 0})]
        for document in documents:
            job_titles.append(*list(document.values()))
        job_titles = set(job_titles)
        return list(job_titles)

    async def find_many_within_search(
            self,
            params_for_search: List[Dict[str, Dict[str, str]]],
            offset: int,
            limit: int
    ) -> List[object_model]:
        return [
            document async for document in
            self.collection.find({"$and": params_for_search})
            .skip(offset)
            .limit(limit)
        ]

    async def find_many_within_search_time(
            self,
            start_time: int,
            end_time: int,
            offset: int,
            limit: int
    ) -> List[object_model]:
        return [
            document async for document in
            self.collection.find({"created": {
                '$gte': start_time,
                '$lt': end_time
            }})
            .skip(offset)
            .limit(limit)
        ]

    async def get_all(self, limit) -> List[object_model]:
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
