import uuid

import sqlalchemy
from packaging import version
from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

if version.parse(sqlalchemy.__version__) >= version.parse("1.4"):

    class User(Base):
        __tablename__ = "user"
        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
        uid: Mapped[int] = mapped_column(Integer)
        name: Mapped[str] = mapped_column(String(255))
        description: Mapped[str] = mapped_column(String(255))
        account: Mapped[str] = mapped_column(String(255))
        password: Mapped[str] = mapped_column(String(255))

else:

    class User(Base):
        __tablename__ = "user"
        id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
        uid = Column(Integer)
        name = Column(String(255))
        description = Column(String(255))
        account = Column(String(255))
        password = Column(String(255))
