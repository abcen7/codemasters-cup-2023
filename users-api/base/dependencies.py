from bson import ObjectId
from typing import NoReturn

from .exceptions import InvalidObjectId, DocumentNotFound
from .models import BaseModelWithConfig


async def is_valid_object_id(object_id: str) -> NoReturn:
    """
    Checking that ObjectId is valid
    """
    if not ObjectId.is_valid(object_id):
        raise InvalidObjectId(object_id)


async def is_document_found(
    my_object: BaseModelWithConfig | None,
) -> BaseModelWithConfig | None:
    if not my_object:
        raise DocumentNotFound()
    return my_object
