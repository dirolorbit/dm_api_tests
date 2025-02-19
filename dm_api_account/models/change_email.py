from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(description="User login")
    password: str = Field(description="User password")
    email: str = Field(description="New user email")
