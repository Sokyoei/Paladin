import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import CreateUpdateAtMixin, UUIDMixin

if TYPE_CHECKING:
    from .user import User


class APIKey(UUIDMixin, CreateUpdateAtMixin):
    __tablename__ = "apikey"
    key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False, comment="API Key")
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, comment="用户 ID"
    )

    user: Mapped["User"] = relationship("User", back_populates="api_keys")
