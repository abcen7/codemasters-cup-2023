from pydantic import Field, validator
from typing import Optional

from base import BaseModelWithConfig
from .utils import get_current_time_in_unix_format


class UpdateUser(BaseModelWithConfig):
    is_admin: Optional[bool] = Field(default=None)
    updated: Optional[float] = Field(default=None, validate_default=True)

    @validator("updated", pre=True, check_fields=False)
    def set_updated_time(
            cls, _: float
    ) -> float:
        return get_current_time_in_unix_format()


class SearchEmployee(BaseModelWithConfig):
    name: Optional[str] = Field(default=None)
    patronymic: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    job_title: Optional[str] = Field(default=None)
    project: Optional[str] = Field(default=None)
