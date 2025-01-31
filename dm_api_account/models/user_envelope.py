from datetime import datetime
from enum import Enum
from typing import (
    List,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class UseRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULATOR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool = Field(description="Rating participation flag")
    quality: int = Field(description="Quality rating")
    quantity: int = Field(description="Quantity rating")


class User(BaseModel):
    login: str = Field(description="User login")
    roles: List[UseRole] = Field(description="User roles")
    medium_picture_url: str = Field(None, description="Profile picture URL M-size", alias='mediumPictureUrl')
    small_picture_url: str = Field(None, description="Profile picture URL S-size", alias='smallPictureUrl')
    status: str = Field(None, description="User defined status")
    rating: Rating
    online: datetime = Field(None, description="Last seen online moment")
    name: str = Field(None, description="User real name")
    location: str = Field(None, description="User real location")
    registration: datetime = Field(None, description="User registration moment")


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: User
    metadata: Union[dict, str] = Field(None, description="Additional metadata")
