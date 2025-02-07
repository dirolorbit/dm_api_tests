from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(description="User login")
    password: str = Field(description="User password")
    remember_me: bool = Field(description="Remember Me option", default=True, serialization_alias="rememberMe")
