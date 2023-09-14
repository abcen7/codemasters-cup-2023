from database import Employees
from bson import ObjectId
from typing import NoReturn

from .exceptions import InvalidObjectId, DocumentNotFound
from .models import Employee


async def get_employee(id: int):
    return await is_document_found(
        await Employees.find_one({"telegram_id": id})
    )


async def is_valid_object_id(object_id: str) -> NoReturn:
    if not ObjectId.is_valid(object_id):
        raise InvalidObjectId(object_id)


async def is_document_found(
        my_object: Employee | None,
) -> Employee | None:
    if not my_object:
        raise DocumentNotFound()
    return my_object
