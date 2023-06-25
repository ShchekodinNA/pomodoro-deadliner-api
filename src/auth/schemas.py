from typing import Optional
from pydantic import BaseModel, Field

password_field = Field(max_length=40, min_length=6, default=None)
username_field = Field(
    regex=r"(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$", max_length=20, min_length=5, default=None
)


class CreateUserOuter(BaseModel):
    username: str = username_field
    email: str
    is_active: bool = True
    user_role_id: int
    password: str = password_field


class ReadUser(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    user_role_id: int


class UpdateUser(BaseModel):
    id: int
    username: Optional[str] = username_field
    email: Optional[str] = None
    is_active: Optional[bool] = None
    user_role_id: Optional[int] = None
    password: Optional[str] = password_field
5