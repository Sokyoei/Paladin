from __future__ import annotations

from typing import TypeVar

from rest_framework import status
from rest_framework.response import Response

T = TypeVar('T')


class ApiResponse(object):

    def __init__(self, code: int, message: str, data: T | None = None):
        self.code = code
        self.message = message
        self.data = data

    def to_response(self, status_code: int | None = None) -> Response:
        return Response(
            data={'code': self.code, 'message': self.message, 'data': self.data}, status=status_code or self.code
        )

    @classmethod
    def success(cls, data: T | None = None) -> ApiResponse:
        return cls(code=status.HTTP_200_OK, message='success', data=data)

    @classmethod
    def fail(cls, message: str, data: T | None = None) -> ApiResponse:
        return cls(code=status.HTTP_400_BAD_REQUEST, message=message, data=data)

    fail_400 = fail

    @classmethod
    def fail_401(cls, message: str = "401 Unauthorized", data: T | None = None) -> ApiResponse:
        return cls(code=status.HTTP_401_UNAUTHORIZED, message=message, data=data)

    @classmethod
    def fail_403(cls, message: str = "403 Forbidden", data: T | None = None) -> ApiResponse:
        return cls(code=status.HTTP_403_FORBIDDEN, message=message, data=data)

    @classmethod
    def fail_404(cls, message: str = "404 Not Found", data: T | None = None) -> ApiResponse:
        return cls(code=status.HTTP_404_NOT_FOUND, message=message, data=data)

    @classmethod
    def fail_405(cls, message: str = "405 Method Not Allowed", data: T | None = None) -> ApiResponse:
        return cls(code=status.HTTP_405_METHOD_NOT_ALLOWED, message=message, data=data)

    @classmethod
    def error(cls, message: str, data: T | None = None) -> ApiResponse:
        return cls(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message, data=data)

    error_500 = error

    @classmethod
    def error_503(cls, message: str = "503 Service Unavailable", data: T | None = None) -> ApiResponse:
        return cls(code=status.HTTP_503_SERVICE_UNAVAILABLE, message=message, data=data)
