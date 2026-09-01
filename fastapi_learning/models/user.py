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
        uid: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False, comment="用户 UID")
        name: Mapped[str] = mapped_column(String(255), comment="用户名")
        description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="用户描述、个人签名")
        account: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, comment="账户")
        hashed_password: Mapped[str] = mapped_column(String(255), comment="哈希密码")
        email: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True, comment="邮箱")

        api_keys: Mapped[list["APIKey"]] = relationship("APIKey", back_populates="user")

else:
    from sqlalchemy import Column

    class User(UUIDMixin, CreateUpdateAtMixin):
        __tablename__ = "user"
        uid = Column(BigInteger, unique=True, index=True, nullable=False, comment="用户 UID")
        name = Column(String(255), comment="用户名")
        description = Column(String(255), nullable=True, comment="用户描述、个人签名")
        account = Column(String(100), unique=True, index=True, nullable=False, comment="账户")
        hashed_password = Column(String(255), comment="哈希密码")
        email = Column(String(100), unique=True, index=True, nullable=True, comment="邮箱")

        api_keys = relationship("APIKey", back_populates="user")
