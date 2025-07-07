from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+aiomysql://root:ahri@localhost:3306/paladin?charset=utf8mb4"


# class Database(object):

#     def __init__(self):
#         self.connection_is_active = False
#         self.engine = None

#     async def get_db_connection(self):
#         if not self.connection_is_active:
#             try:
#                 self.engine = create_async_engine(DATABASE_URL)
#                 self.connection_is_active = True
#                 yield self.engine
#             except Exception as e:
#                 logger.error(e)
#         yield self.engine

#     async def get_db_session(self, engine):
#         session = sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)
#         async with session() as sess:
#             yield sess


# conn = Database().get_db_connection()
# db = Database().get_db_session(conn)


class Database:
    __instance = None
    __engine = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__engine = create_async_engine(DATABASE_URL)
        return cls.__instance

    @property
    def engine(self):
        return self.__engine

    async def get_db_session(self):
        """异步生成器：创建并管理数据库会话"""
        async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"数据库错误: {e}")
                raise
            finally:
                await session.close()


db_instance = Database()


async def get_db():
    async for session in db_instance.get_db_session():
        yield session
