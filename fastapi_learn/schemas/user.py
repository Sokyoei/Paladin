from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(description="用户 UID")
    name: str = Field(description="用户名")
    description: str = Field(description="用户描述")
    account: str = Field(description="用户账号")
    password: str = Field(description="用户密码")
