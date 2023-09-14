from pydantic import Field, BaseModel, ConfigDict, validator
from typing import Optional, List
from bson import ObjectId

from base import BaseModelWithConfig
from .utils import get_current_time_in_unix_format


class User(BaseModelWithConfig):

    id: Optional[str] = Field(default=None, alias="_id", validate_default=True)
    telegram_id: int = Field()
    created: Optional[float] = Field(default=None, validate_default=True)
    updated: Optional[float] = Field(default=None, validate_default=True)

    @validator("id", pre=True, check_fields=False)
    def convert_object_id_in_str(cls, v: ObjectId) -> str:
        return str(v)

    @validator("created_at", "updated_at", pre=True, check_fields=False)
    def init_create_and_update_time(cls, v: float) -> float:
        """
        The creation and update time is set once
        """
        return v or get_current_time_in_unix_format()