from .models import Employee
from .repositories import EmployeesRepository
from .schemas import UpdateEmployee, SearchEmployee

from typing import List

from .utils import prepare_model_for_search_query


class EmployeesService:
    object_model = Employee

    def __init__(self) -> None:
        self.repository = EmployeesRepository()

    async def find_many_within_search(self, params_for_search: SearchEmployee) -> List[object_model]:
        return await self.repository.find_many_within_search(
            prepare_model_for_search_query(params_for_search.model_dump(exclude_none=True))
        )

    async def get_all(self, limit: int = 20) -> List[object_model]:
        return await self.repository.get_all(limit)

    async def get_one(self, object_id: str) -> object_model:
        return await self.repository.get_by_id(object_id)

    async def create(self, create_object: object_model) -> object_model:
        return await self.repository.create(create_object.model_dump(exclude_none=True))

    async def delete(self, object_id: str) -> object_model:
        return await self.repository.delete(object_id)

    async def update(self, employee_id: str, params_for_update: UpdateEmployee) -> object_model:
        return await self.repository.update(
            employee_id,
            params_for_update.model_dump(exclude_none=True)
        )
