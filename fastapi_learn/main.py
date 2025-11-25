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
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from fastapi_learn.api import all_routers
from fastapi_learn.config import db_instance, websocket_manager
from fastapi_learn.utils import ApiResponse, register_exception_handlers

apirouter = APIRouter()


########################################################################################################################
# router
########################################################################################################################
@apirouter.get("/")
async def index():
    return {"hello": "world"}


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
async def upload(file: UploadFile = File(...)):
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
    username: str | None = Form(None, description="用户名"),
    message: str | None = Form(None, description="消息"),
):
    templates = cast(Jinja2Templates, app.state.templates)
    result = {"username": username, "message": message} if request.method == "POST" and (username and message) else {}
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
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start FastAPI")

    # router
    app.include_router(apirouter)
    for router in all_routers:
        app.include_router(router)
    # mount
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")
    # template
    app.state.templates = Jinja2Templates(directory="templates")

    await db_instance.init_db()
    yield
    await db_instance.close_db()

    logger.info("Close FastAPI")


app = FastAPI(lifespan=lifespan, debug=True)
# add middleware when app is started
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产请严格限制
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
register_exception_handlers(app)


def main():
    uvicorn.run(
        app="main:app",
        reload=True,
        # workers=4,  # 多线程与 debug(reload=True) 冲突
    )


if __name__ == "__main__":
    main()
