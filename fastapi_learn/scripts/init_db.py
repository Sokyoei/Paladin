import asyncio

from fastapi_learn.config import db_instance

if __name__ == '__main__':
    asyncio.run(db_instance.init_db())
