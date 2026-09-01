from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from django_learning.utils.django_utils import ApiResponse


class ApiResponseExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request: HttpRequest, exception: Exception):
        if isinstance(exception, PermissionDenied):
            return ApiResponse.fail_403("权限不足").to_jsonresponse()

        elif isinstance(exception, ObjectDoesNotExist):
            return ApiResponse.fail_404("资源不存在").to_jsonresponse()

        elif isinstance(exception, ValidationError):
            return ApiResponse.fail("验证错误", data=exception.message_dict).to_jsonresponse()

        message = f"{type(exception).__name__}: {exception!s}" if settings.DEBUG else "服务器内部错误"

        return ApiResponse.error(message).to_jsonresponse()
