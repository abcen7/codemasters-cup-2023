from typing import List
from pydantic import BaseModel


class BaseService:
    object_model = BaseModel

    def __init__(self, object_repository) -> None:
        self.repository = object_repository()

    async def get_all(self) -> List[object_model]:
        return await self.repository.get_all()

    async def get_one(self, object_id: str) -> object_model:
        return await self.repository.get_by_id(object_id)

    async def create(self, create_object: object_model) -> object_model:
        return await self.repository.create(create_object.model_dump(exclude_none=True))

    async def delete(self, object_id: str) -> object_model:
        return await self.repository.delete(object_id)
