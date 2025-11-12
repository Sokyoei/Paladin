import sqlalchemy
from packaging import version
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

if version.parse(sqlalchemy.__version__) >= version.parse("1.4"):

    class User(Base):
        __tablename__ = "users"
        id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
        name: Mapped[str] = mapped_column(String(255))
        description: Mapped[str] = mapped_column(String(255))
        account: Mapped[str] = mapped_column(String(255))
        password: Mapped[str] = mapped_column(String(255))

else:

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String(255))
        description = Column(String(255))
        account = Column(String(255))
        password = Column(String(255))
