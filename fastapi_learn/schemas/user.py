import uuid
from typing import Annotated, Optional

from pydantic import BaseModel, Field

User_id = Annotated[uuid.UUID, Field(description="用户 UUID")]
User_uid = Annotated[int, Field(description="用户 UID")]
User_name = Annotated[str, Field(description="用户名")]
User_description = Annotated[str, Field(description="用户描述")]
User_account = Annotated[str, Field(description="用户账号")]
User_password = Annotated[str, Field(description="用户密码")]


class UserCreate(BaseModel):
    uid: User_uid
    name: User_name
    description: Optional[User_description] = None
    account: User_account
    password: User_password


class UserResponse(UserCreate):
    id: User_id


class UserUpdate(BaseModel):
    id: User_id
    uid: Optional[User_uid] = None
    name: Optional[User_name] = None
    description: Optional[User_description] = None
    account: Optional[User_account] = None
    password: Optional[User_password] = None
