import uuid

import sqlalchemy
from packaging import version
from sqlalchemy import UUID, BigInteger, Column, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

if version.parse(sqlalchemy.__version__) >= version.parse("1.4"):

    class User(Base):
        __tablename__ = "user"
        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
        uid: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
        name: Mapped[str] = mapped_column(String(255))
        description: Mapped[str | None] = mapped_column(String(255), nullable=True)
        account: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
        password: Mapped[str] = mapped_column(String(255))
        email: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)

else:

    class User(Base):
        __tablename__ = "user"
        id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
        uid = Column(BigInteger, unique=True, index=True, nullable=False)
        name = Column(String(255))
        description = Column(String(255), nullable=True)
        account = Column(String(100), unique=True, index=True, nullable=False)
        password = Column(String(255))
        email = Column(String(100), unique=True, index=True, nullable=True)
