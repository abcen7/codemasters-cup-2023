from pydantic import Field, validator
from typing import Optional
from bson import ObjectId
from .utils import get_current_time_in_unix_format
from base import BaseModelWithConfig


class Employee(BaseModelWithConfig):
    id: str = Field(alias="_id", default=None)
    name: str = Field()
    patronymic: Optional[str] = Field(default=None)
    surname: str = Field()
    job_title: str = Field()
    project: str = Field()
    avatar_path: Optional[str] = Field(default=None)
    created: Optional[float] = Field(default=None, validate_default=True)
    updated: Optional[float] = Field(default=None, validate_default=True)

    @validator("id", pre=True, check_fields=False)
    def convert_object_id_in_str(cls, v: ObjectId) -> str:
        return str(v)

    @validator("created", "updated", pre=True, check_fields=False)
    def init_create_and_update_time(cls, v: float) -> float:
        """
        The creation and update time is set once
        """
        return v or get_current_time_in_unix_format()
