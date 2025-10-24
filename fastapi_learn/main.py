from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from loguru import logger

from fastapi_learn.api import all_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("start fastapi")

    for router in all_routers:
        app.include_router(router)

    # app.mount("/static", StaticFiles(directory="static"), name="static")
    # async_redis_config = AsyncRedisConfig()
    # await async_redis_config.start()
    yield
    # await async_redis_config.close()
    logger.info("close fastapi")


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


def main():
    uvicorn.run(
        app="main:app",
        reload=True,
        # workers=4,  # 多线程与 debug(reload=True) 冲突
    )


if __name__ == "__main__":
    main()
