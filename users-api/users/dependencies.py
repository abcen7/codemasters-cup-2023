from bson import ObjectId
from typing import NoReturn

from .exceptions import InvalidObjectId, DocumentNotFound
from .models import User


async def get_user(telegram_data: str, telegram_id: int):
    return await is_document_found(
        await Users.find_one({"telegram_id": telegram_id})
    )


async def is_valid_object_id(object_id: str) -> NoReturn:
    if not ObjectId.is_valid(object_id):
        raise InvalidObjectId(object_id)


async def is_document_found(
        my_object: User | None,
) -> User | None:
    if not my_object:
        raise DocumentNotFound()
    return my_object
