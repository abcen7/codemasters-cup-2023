from pydantic import BaseModel, ConfigDict
from bson import ObjectId


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
