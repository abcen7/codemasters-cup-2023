from fastapi import APIRouter, Depends
from starlette import status
from typing import List

from .services import EmployeesService
from .models import Employee
from .dependencies import is_valid_object_id, get_employee
from .schemas import UpdateEmployee, SearchEmployee

employees_router = APIRouter()


@employees_router.post(
    "/search/employees",
    status_code=status.HTTP_200_OK,
)
async def get_employees_within_search(
        offset: int,
        limit: int,
        params_for_search: SearchEmployee,
        employees_service: EmployeesService = Depends(),
) -> List[Employee]:
    return await employees_service.find_many_within_search(params_for_search, offset, limit)


@employees_router.post(
    "/search/employees/time",
    status_code=status.HTTP_200_OK,
)
async def get_employees_within_search_time(
        offset: int,
        limit: int,
        params_for_search: SearchEmployee,
        employees_service: EmployeesService = Depends(),
) -> List[Employee]:
    return await employees_service.find_many_within_search_time(params_for_search, offset, limit)



@employees_router.get(
    "/employees/job_titles",
    status_code=status.HTTP_200_OK,
)
async def get_all_employees(
        employees_service: EmployeesService = Depends(),
) -> List[str]:
    return await employees_service.get_all_job_titles()



@employees_router.get(
    "/employees",
    status_code=status.HTTP_200_OK,
)
async def get_all_employees(
        employees_service: EmployeesService = Depends(),
        limit: int = 20
) -> List[Employee]:
    return await employees_service.get_all(limit)


@employees_router.get(
    "/employees/{object_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(is_valid_object_id)],
)
async def get_one_employee(
        object_id: str,
        employees_service: EmployeesService = Depends()
) -> Employee:
    return await employees_service.get_one(object_id)


@employees_router.post(
    "/employees",
    status_code=status.HTTP_201_CREATED
)
async def create_employee(
        employee: Employee,
        employees_service: EmployeesService = Depends()
) -> Employee:
    return await employees_service.create(employee)


@employees_router.delete(
    "/employees/{id}",
    status_code=status.HTTP_200_OK,
)
async def delete_employee(
        id: str,
        employees_service: EmployeesService = Depends()
) -> Employee:
    return await employees_service.delete(id)


@employees_router.patch(
    "/employees/{id}",
    status_code=status.HTTP_200_OK,
)
async def update_employee(
        id: str,
        params_for_updates: UpdateEmployee,
        employees_service: EmployeesService = Depends()
) -> Employee:
    return await employees_service.update(id, params_for_updates)
