import uuid
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import CreateUpdateAtMixin, UUIDMixin

if TYPE_CHECKING:
    from .user import User


class APIKey(UUIDMixin, CreateUpdateAtMixin):
    __tablename__ = "apikey"
    key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False, comment="API Key")
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey("user.id", ondelete="cascade"), nullable=False, comment="用户 ID"
    )

    user: Mapped["User"] = relationship("User", back_populates="api_keys")
