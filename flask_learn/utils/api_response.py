from http import HTTPStatus
from typing import Generic, TypeVar

from flask import jsonify
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: T | None = None

    @classmethod
    def success(cls, data: T | None = None) -> 'ApiResponse[T]':
        return jsonify(cls(code=HTTPStatus.OK.value, message='success', data=data)), cls.code

    @classmethod
    def fail(cls, message: str, data: T | None = None) -> 'ApiResponse[T]':
        return jsonify(cls(code=HTTPStatus.BAD_REQUEST.value, message=message, data=data)), cls.code

    @classmethod
    def error(cls, message: str, data: T | None = None) -> 'ApiResponse[T]':
        return jsonify(cls(code=HTTPStatus.INTERNAL_SERVER_ERROR.value, message=message, data=data)), cls.code
