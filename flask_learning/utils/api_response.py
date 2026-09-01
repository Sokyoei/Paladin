from http import HTTPStatus

from flask import jsonify
from pydantic import BaseModel


class ApiResponse[T](BaseModel):
    code: int
    message: str
    data: T | None = None

    def to_flask(self):
        return jsonify(self.model_dump()), self.code

    @classmethod
    def success(cls, data: T | None = None):
        response = cls(code=HTTPStatus.OK.value, message="success", data=data)
        return response.to_flask()

    @classmethod
    def fail(cls, message: str, data: T | None = None):
        response = cls(code=HTTPStatus.BAD_REQUEST.value, message=message, data=data)
        return response.to_flask()

    @classmethod
    def error(cls, message: str, data: T | None = None):
        response = cls(code=HTTPStatus.INTERNAL_SERVER_ERROR.value, message=message, data=data)
        return response.to_flask()
