from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from fastapi_learn.api import item_router, user_router
from fastapi_learn.config import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("start fastapi")
    app.include_router(item_router)
    app.include_router(user_router)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    db = Database().get_db_connection()  # noqa: F841
    # async_redis_config = AsyncRedisConfig()
    # await async_redis_config.start()
    yield
    # await async_redis_config.close()
    logger.info("close fastapi")


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")


def main():
    uvicorn.run(app="main:app", reload=True)


if __name__ == '__main__':
    main()
