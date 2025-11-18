import json
import time
from contextlib import asynccontextmanager
from typing import cast

import uvicorn
from fastapi import APIRouter, FastAPI, File, Form, HTTPException, Request, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from fastapi_learn.api import all_routers
from fastapi_learn.config import db_instance, websocket_manager
from fastapi_learn.schemas import Response

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
    return Response.success()


@apirouter.get("/websocket")
def websocket_html(request: Request):
    templates = cast(Jinja2Templates, app.state.templates)
    return templates.TemplateResponse("websocket.html", {"request": request})


@apirouter.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Client `{client_id}` receive data: {data}")
            await websocket_manager.send_message(data, client_id)
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
    except Exception as e:
        logger.error(e)
        websocket_manager.disconnect(client_id)


@apirouter.get("/form")
@apirouter.post("/form")
async def form_html(request: Request, username: str = Form(None), message: str = Form(None)):
    templates = cast(Jinja2Templates, app.state.templates)
    result = {"username": username, "message": message} if username and message else {}
    return templates.TemplateResponse("form.html", {"request": request, "result": result})


########################################################################################################################
# app
########################################################################################################################
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("start fastapi")

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

    logger.info("close fastapi")


app = FastAPI(lifespan=lifespan, debug=True)
# add middleware when app is started
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产请严格限制
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        exc: HTTPException
        if isinstance(exc.detail, str):
            if 400 <= exc.status_code < 500:
                return Response.fail(message=exc.detail)
            else:
                return Response.error(message=exc.detail)
        if isinstance(exc.detail, Response):
            return exc.detail

    message = str(exc) if app.debug else ""
    return Response.error(message)


def main():
    uvicorn.run(
        app="main:app",
        reload=True,
        # workers=4,  # 多线程与 debug(reload=True) 冲突
    )


if __name__ == "__main__":
    main()
