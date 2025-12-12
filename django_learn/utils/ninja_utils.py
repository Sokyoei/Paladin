from __future__ import annotations

import uuid
from http import HTTPStatus
from typing import Generic, TypeVar

from ninja import Field, Schema

T = TypeVar("T")


########################################################################################################################
# Schemas
########################################################################################################################
class UUIDSchema(Schema):
    id: uuid.UUID = Field(description="Unique Identifier")


class CreateUpdateAtSchema(Schema):
    created_at: str = Field(description="Created At")
    updated_at: str = Field(description="Updated At")


class CreateUpdateBySchema(Schema):
    created_by: str = Field(description="Created By")
    updated_by: str = Field(description="Updated By")


########################################################################################################################
# API Response
########################################################################################################################
class ApiResponse(Schema, Generic[T]):
    code: int = Field(description="状态码")
    message: str = Field(description="消息")
    data: T | None = Field(default=None, description="数据")

    @classmethod
    def success(cls, data: T | None = None) -> ApiResponse[T]:
        return cls(code=HTTPStatus.OK.value, message="success", data=data)

    @classmethod
    def fail(cls, message: str, data: T | None = None) -> ApiResponse[T]:
        return cls(code=HTTPStatus.BAD_REQUEST.value, message=message, data=data)

    fail_400 = fail

    @classmethod
    def fail_401(cls, message: str = "401 Unauthorized", data: T | None = None) -> ApiResponse[T]:
        return cls(code=HTTPStatus.UNAUTHORIZED.value, message=message, data=data)

    @classmethod
    def fail_403(cls, message: str = "403 Forbidden", data: T | None = None) -> ApiResponse[T]:
        return cls(code=HTTPStatus.FORBIDDEN.value, message=message, data=data)

    @classmethod
    def fail_404(cls, message: str = "404 Not Found", data: T | None = None) -> ApiResponse[T]:
        return cls(code=HTTPStatus.NOT_FOUND.value, message=message, data=data)

    @classmethod
    def fail_405(cls, message: str = "405 Method Not Allowed", data: T | None = None) -> ApiResponse[T]:
        return cls(code=HTTPStatus.METHOD_NOT_ALLOWED.value, message=message, data=data)

    @classmethod
    def error(cls, message: str, data: T | None = None) -> ApiResponse[T]:
        return cls(code=HTTPStatus.INTERNAL_SERVER_ERROR.value, message=message, data=data)

    error_500 = error

    @classmethod
    def error_503(cls, message: str = "503 Service Unavailable", data: T | None = None) -> ApiResponse[T]:
        return cls(code=HTTPStatus.SERVICE_UNAVAILABLE.value, message=message, data=data)
