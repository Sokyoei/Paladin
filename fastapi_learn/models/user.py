from typing import TYPE_CHECKING

import sqlalchemy
from packaging import version
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import CreateUpdateAtMixin, UUIDMixin

if TYPE_CHECKING:
    from .apikey import APIKey

if version.parse(sqlalchemy.__version__) >= version.parse("1.4"):

    class User(UUIDMixin, CreateUpdateAtMixin):
        __tablename__ = "user"
        uid: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
        name: Mapped[str] = mapped_column(String(255))
        description: Mapped[str | None] = mapped_column(String(255), nullable=True)
        account: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
        password: Mapped[str] = mapped_column(String(255))
        email: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)

        api_keys: Mapped[list["APIKey"]] = relationship("APIKey", back_populates="user")

else:
    from sqlalchemy import Column

    class User(UUIDMixin, CreateUpdateAtMixin):
        __tablename__ = "user"
        uid = Column(BigInteger, unique=True, index=True, nullable=False)
        name = Column(String(255))
        description = Column(String(255), nullable=True)
        account = Column(String(100), unique=True, index=True, nullable=False)
        password = Column(String(255))
        email = Column(String(100), unique=True, index=True, nullable=True)

        api_keys = relationship("APIKey", back_populates="user")
