from typing import AsyncGenerator, Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from fastapi_learn.models import Base

from .config import SQLALCHEMY_DATABASE_URL


class Database(object):
    __instance: Optional["Database"] = None
    __engine = None
    __async_sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__engine = create_async_engine(
                SQLALCHEMY_DATABASE_URL,
                echo=True,  # 打印 SQL 语句
                pool_pre_ping=True,  # 检查连接是否可用，避免失效连接
                pool_recycle=3600,  # 连接1小时自动回收，避免长时间空闲
                pool_size=10,  # 连接池默认大小（每个进程）
                max_overflow=20,  # 连接池最大溢出数（每个进程）
                connect_args={"check_same_thread": False},  # aiosqlite 必须配置（关闭线程检查）
            )
            cls.__async_sessionmaker = async_sessionmaker(
                cls.__engine,
                class_=AsyncSession,
                expire_on_commit=False,  # 提交后不失效对象，便于后续访问
                autoflush=False,  # 关闭自动刷新，避免意外提交
                autocommit=False,  # 关闭自动提交，避免意外提交
            )
        return cls.__instance

    @property
    def engine(self):
        if not self.__engine:
            raise RuntimeError("数据库引擎未初始化")
        return self.__engine

    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        """异步生成器：创建并管理数据库会话"""
        if not self.__async_sessionmaker:
            raise RuntimeError("数据库会话工厂未初始化")

        async with self.__async_sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"数据库错误: {e}")
                raise
            finally:
                await session.close()

    async def get_manual_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self.__async_sessionmaker:
            raise RuntimeError("数据库会话工厂未初始化")

        async with self.__async_sessionmaker() as session:
            try:
                yield session
            finally:
                await session.close()

    async def init_db(self):
        """初始化数据库"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库初始化完成")

    async def close_db(self):
        if self.__engine:
            await self.__engine.dispose()
            logger.info("数据库已关闭")


db_instance = Database()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_instance.get_db_session():
        yield session


async def get_manual_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_instance.get_manual_db_session():
        yield session
