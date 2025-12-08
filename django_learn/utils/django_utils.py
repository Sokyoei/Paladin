from __future__ import annotations

import uuid
from http import HTTPStatus
from typing import Any, Dict, TypeVar

from django.db import models
from django.http import JsonResponse

T = TypeVar('T')


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class CreateUpdateAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CreateUpdateByModel(models.Model):
    created_by = models.UUIDField(null=True, blank=True)
    updated_by = models.UUIDField(null=True, blank=True)


class ApiResponse(object):

    def __init__(self, code: int, message: str, data: T | None = None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {'code': self.code, 'message': self.message, 'data': self.data}

    def to_jsonresponse(self, status_code: int | None = None) -> JsonResponse:
        return JsonResponse(
            data=self.to_dict(), status=status_code or self.code, json_dumps_params={'ensure_ascii': False}
        )

    @classmethod
    def success(cls, data: T | None = None) -> ApiResponse:
        return cls(code=HTTPStatus.OK.value, message='success', data=data)

    @classmethod
    def fail(cls, message: str, data: T | None = None) -> ApiResponse:
        return cls(code=HTTPStatus.BAD_REQUEST.value, message=message, data=data)

    fail_400 = fail

    @classmethod
    def fail_401(cls, message: str = "401 Unauthorized", data: T | None = None) -> ApiResponse:
        return cls(code=HTTPStatus.UNAUTHORIZED.value, message=message, data=data)

    @classmethod
    def fail_403(cls, message: str = "403 Forbidden", data: T | None = None) -> ApiResponse:
        return cls(code=HTTPStatus.FORBIDDEN.value, message=message, data=data)

    @classmethod
    def fail_404(cls, message: str = "404 Not Found", data: T | None = None) -> ApiResponse:
        return cls(code=HTTPStatus.NOT_FOUND.value, message=message, data=data)

    @classmethod
    def fail_405(cls, message: str = "405 Method Not Allowed", data: T | None = None) -> ApiResponse:
        return cls(code=HTTPStatus.METHOD_NOT_ALLOWED.value, message=message, data=data)

    @classmethod
    def error(cls, message: str, data: T | None = None) -> ApiResponse:
        return cls(code=HTTPStatus.INTERNAL_SERVER_ERROR.value, message=message, data=data)

    error_500 = error

    @classmethod
    def error_503(cls, message: str = "503 Service Unavailable", data: T | None = None) -> ApiResponse:
        return cls(code=HTTPStatus.SERVICE_UNAVAILABLE.value, message=message, data=data)
