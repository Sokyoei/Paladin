import uuid
from typing import Annotated

from fastapi_users import schemas
from pydantic import EmailStr, Field

User_id = Annotated[uuid.UUID, Field(description="用户 UUID")]
User_uid = Annotated[int, Field(description="用户 UID")]
User_name = Annotated[str, Field(description="用户名")]
User_description = Annotated[str | None, Field(description="用户描述")]
User_phone = Annotated[str | None, Field(description="手机号")]
User_password = Annotated[str, Field(description="用户密码")]
User_hashed_password = Annotated[str, Field(description="用户密码哈希值")]
User_email = Annotated[EmailStr | None, Field(description="用户邮箱（可选）")]


class UserCreate(schemas.BaseUserCreate):
    name: User_name
    description: User_description = None
    phone: User_phone = None
    password: User_password
    email: User_email = None


class UserResponse(schemas.BaseUser[uuid.UUID]):
    id: User_id
    uid: User_uid
    name: User_name
    description: User_description
    phone: User_phone
    email: User_email


class UserUpdate(schemas.BaseUserUpdate):
    name: User_name | None = None
    description: User_description | None = None
    phone: User_phone = None
    password: User_password | None = None
    email: User_email = None
