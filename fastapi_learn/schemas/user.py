import uuid
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

User_id = Annotated[uuid.UUID, Field(description="用户 UUID")]
User_uid = Annotated[int, Field(description="用户 UID")]
User_name = Annotated[str, Field(description="用户名")]
User_description = Annotated[str | None, Field(description="用户描述")]
User_account = Annotated[str, Field(description="用户账号")]
User_password = Annotated[str, Field(description="用户密码")]
User_email = Annotated[EmailStr | None, Field(description="用户邮箱")]


class UserCreate(BaseModel):
    name: User_name
    description: User_description = None
    account: User_account
    password: User_password
    email: User_email = None


class UserResponse(BaseModel):
    id: User_id
    uid: User_uid
    name: User_name
    description: User_description
    account: User_account
    email: User_email


class UserUpdate(BaseModel):
    name: User_name | None = None
    description: User_description | None = None
    # account: User_account | None = None
    password: User_password | None = None
    email: User_email | None = None
