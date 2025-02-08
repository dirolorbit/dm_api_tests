from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class BbParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULATOR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class Rating(BaseModel):
    enabled: bool = Field(description="Rating participation flag")
    quality: int = Field(description="Quality rating")
    quantity: int = Field(description="Quantity rating")


class InfoBbText(BaseModel):
    value: str = Field(description="Text")
    parse_mode: BbParseMode = Field(description="BB text parse mode", alias="parseMode")


class Paging(BaseModel):
    posts_per_page: int = Field(
        description="Number of posts on a game room page",
        alias='postsPerPage'
    )
    comments_per_page: int = Field(
        description="Number of commentaries on a game or a topic page",
        alias='commentsPerPage'
    )
    topics_per_page: int = Field(
        description="Number of detached topics on a forum page",
        alias='topicsPerPage'
    )
    messages_per_page: int = Field(
        description="Number of private messages and conversations on dialogue page",
        alias='messagesPerPage'
    )
    entities_per_page: int = Field(
        description="Number of other entities on page",
        alias='entitiesPerPage'
    )


class UserSettings(BaseModel):
    colorSchema: ColorSchema
    nannyGreetingsMessage: str = Field(
        None, description="Message that user's newbies will receive once "
                          "they are connected"
    )
    paging: Paging


class UserDetails(BaseModel):
    login: str = Field(description="User login")
    roles: List[UserRole] = Field(description="User roles")
    medium_picture_url: str = Field(None, description="Profile picture URL M-size", alias='mediumPictureUrl')
    small_picture_url: str = Field(None, description="Profile picture URL S-size", alias='smallPictureUrl')
    status: str = Field(None, description="User defined status")
    rating: Rating
    online: datetime = Field(None, description="Last seen online moment")
    name: str = Field(None, description="User real name")
    location: str = Field(None, description="User real location")
    registration: datetime = Field(None, description="User registration moment")
    icq: str = Field(None, description="User ICQ number")
    skype: str = Field(None, description="User Skype login")
    original_picture_url: str = Field(None, description="URL of profile picture original", alias='originalPictureUrl')
    info: Union[InfoBbText, str] = Field(None)
    settings: Optional[UserSettings] = None


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: UserDetails
    metadata: Union[dict, str] = Field(None, description="Additional metadata")
