from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from Paladin.utils import log

DATABASE_URL = "mysql+aiomysql://root:ahri@localhost:3306/paladin?charset=utf8mb4"


class Database(object):

    def __init__(self):
        self.connection_is_active = False
        self.engine = None

    async def get_db_connection(self):
        if not self.connection_is_active:
            try:
                self.engine = create_async_engine(DATABASE_URL)
                self.connection_is_active = True
                yield self.engine
            except Exception as e:
                log.error(e)
        yield self.engine

    async def get_db_session(self, engine) -> AsyncSession:
        session = sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)
        async with session() as sess:
            yield sess


conn = Database().get_db_connection()
db = Database().get_db_session(conn)
