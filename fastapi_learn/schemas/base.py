from __future__ import annotations

from typing import Generic, Optional, TypeVar

from fastapi import status
from pydantic import BaseModel

T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None

    @classmethod
    def success(cls, data: Optional[T] = None) -> Response[T]:
        return cls(code=status.HTTP_200_OK, message='success', data=data)

    @classmethod
    def fail(cls, message: str, data: Optional[T] = None) -> Response[T]:
        return cls(code=status.HTTP_400_BAD_REQUEST, message=message, data=data)

    @classmethod
    def error(cls, message: str, data: Optional[T] = None) -> Response[T]:
        return cls(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message, data=data)
