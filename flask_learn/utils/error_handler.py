from flask import Flask
from werkzeug.exceptions import HTTPException

from flask_learn.utils.error import PaladinFlaskLearnError

from .api_response import ApiResponse


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(PaladinFlaskLearnError)
    async def paladin_error_handler(exc: PaladinFlaskLearnError):
        return ApiResponse.fail(str(exc))

    @app.errorhandler(HTTPException)
    async def werkzeug_exceptions_handler(exc: HTTPException):
        return ApiResponse(code=exc.code, message=exc.description).to_flask()
