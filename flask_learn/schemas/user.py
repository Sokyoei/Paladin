from pydantic import BaseModel, EmailStr, Field

from .base import CreateUpdateAtSchema, CreateUpdateBySchema, UUIDSchema


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="邮箱")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserResponse(UUIDSchema, CreateUpdateAtSchema, CreateUpdateBySchema):
    email: str = Field(..., description="邮箱")
    username: str = Field(..., description="用户名")


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(None)
    username: str | None = Field(None)
    password: str | None = Field(None)
