from __future__ import annotations

from typing import Generic, TypeVar

from ninja import Field, Schema

T = TypeVar("T")


class ApiResponse(Schema, Generic[T]):
    code: int = Field(description="状态码")
    message: str = Field(description="消息")
    data: T | None = Field(default=None, description="数据")

    @classmethod
    def success(cls, data: T | None = None) -> ApiResponse[T]:
        return cls(code=200, message="success", data=data)

    @classmethod
    def fail(cls, message: str, data: T | None = None) -> ApiResponse[T]:
        return cls(code=400, message=message, data=data)

    @classmethod
    def fail_404(cls, message: str = "404 Not Found", data: T | None = None) -> ApiResponse[T]:
        return cls(code=404, message=message, data=data)

    @classmethod
    def error(cls, message: str, data: T | None = None) -> ApiResponse[T]:
        return cls(code=500, message=message, data=data)
