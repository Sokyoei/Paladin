import json
import time
from contextlib import asynccontextmanager
from typing import Annotated, cast

import uvicorn
from fastapi import (
    APIRouter,
    Cookie,
    FastAPI,
    File,
    Form,
    Header,
    Request,
    Response,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from fastapi_learn import FASTAPILEARN_ROOT
from fastapi_learn.api import all_routers
from fastapi_learn.config import admin_manager, db_instance, settings, websocket_manager
from fastapi_learn.utils import ApiResponse, register_exception_handlers

apirouter = APIRouter()


########################################################################################################################
# router
########################################################################################################################
@apirouter.get("/")
async def index(request: Request):
    templates = cast(Jinja2Templates, app.state.templates)
    return templates.TemplateResponse("index.html", {"request": request})


@apirouter.get("/sse")
async def sse():
    async def generate():
        n = 1
        while True:
            data = {"value": n}
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)
            print(f"send data: {data}")
            n += 1

    return StreamingResponse(generate(), media_type="text/event-stream")


@apirouter.post("/upload")
async def upload(file: Annotated[UploadFile, File(description="上传文件")]):
    with open("temp.data", "wb") as f:
        contents = await file.read()
        f.write(contents)
    return ApiResponse.success()


@apirouter.get("/websocket")
def websocket_html(request: Request):
    templates = cast(Jinja2Templates, app.state.templates)
    return templates.TemplateResponse("websocket.html", {"request": request})


@apirouter.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)

    try:
        async for data in websocket.iter_text():
            logger.info(f"Client `{client_id}` receive data: {data}")
            await websocket_manager.send_message(data, client_id)
    except WebSocketDisconnect:
        await websocket_manager.disconnect(client_id)
    except Exception as e:
        logger.error(e)
        await websocket_manager.disconnect(client_id)


@apirouter.get("/form")
@apirouter.post("/form")
async def form_html(
    request: Request,
    username: Annotated[str | None, Form(description="用户名")] = None,
    message: Annotated[str | None, Form(description="消息")] = None,
):
    templates = cast(Jinja2Templates, app.state.templates)
    result = (
        {"username": username, "message": message}
        if request.method == "POST" and (username is not None and message is not None)
        else {}
    )
    return templates.TemplateResponse("form.html", {"request": request, "result": result})


@apirouter.get("/header")
async def header(user_agent: Annotated[str | None, Header()] = None):
    return {"user_agent": user_agent}


@apirouter.get("/headers")
async def headers(request: Request):
    return {"headers": request.headers}


@apirouter.post("/set_cookie")
async def set_cookie(response: Response):
    response.set_cookie(
        key="session_id",
        value="123456",
        httponly=True,  # 仅 HTTP 访问，禁止 JS 读取（防止 XSS 攻击）
        secure=True,  # 仅 HTTPS 环境生效
        samesite='strict',  # 防止 CSRF 攻击
        max_age=60 * 60 * 24 * 365,
    )
    return ApiResponse.success()


@apirouter.get("/get_cookie")
async def get_cookie(session_id: Annotated[str | None, Cookie(description="会话 ID")] = None):
    return {"session_id": session_id}


########################################################################################################################
# app
########################################################################################################################
def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Start FastAPI")

        await db_instance.init_db()
        yield
        await db_instance.close_db()

        logger.info("Close FastAPI")

    app = FastAPI(lifespan=lifespan, docs_url=None, title="FastAPI Learn")

    if settings.DEBUG:
        app.debug = True

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产请严格限制
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    # router
    app.include_router(apirouter)
    for router in all_routers:
        app.include_router(router)
    # mount
    app.mount("/static", StaticFiles(directory=FASTAPILEARN_ROOT / "fastapi_learn/static"), name="static")
    # template
    app.state.templates = Jinja2Templates(directory="templates")
    # exception handlers
    register_exception_handlers(app)

    # admin
    admin_manager.init_app(app)
    admin_manager.register_models()

    return app


app = create_app()


@app.get("/docs")
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="",
        swagger_favicon_url="/static/assets/favicon.ico",
        swagger_css_url="",
    )


def main():
    uvicorn.run(
        app="main:app",
        reload=True,
        # workers=4,  # 多线程与 debug(reload=True) 冲突
    )


if __name__ == "__main__":
    main()
