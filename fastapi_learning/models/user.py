from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID, SQLAlchemyBaseUserTableUUID
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, CreateUpdateAtMixin

if TYPE_CHECKING:
    from .apikey import APIKey


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(CreateUpdateAtMixin, SQLAlchemyBaseUserTableUUID):
    uid: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False, comment="用户 UID")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="用户名")
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True, comment="手机号")
    description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="用户描述、个人签名")

    if TYPE_CHECKING:
        email: str
    else:
        email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=True, comment="邮箱（可选）")

    api_keys: Mapped[list["APIKey"]] = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined", cascade="all, delete-orphan"
    )
