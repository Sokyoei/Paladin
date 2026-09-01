from fastapi import FastAPI, HTTPException, Request

from . import ApiResponse


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        if isinstance(exc.detail, str):
            return ApiResponse(code=exc.status_code, message=exc.detail).to_orjsonresponse()
        if isinstance(exc.detail, dict):
            message = exc.detail.get("message", exc.detail.get("msg", ""))
            return ApiResponse(code=exc.status_code, message=message).to_orjsonresponse()

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        if isinstance(exc, HTTPException):
            return await http_exception_handler(request, exc)

        message = str(exc) if app.debug else ""
        return ApiResponse.error(message).to_orjsonresponse()
