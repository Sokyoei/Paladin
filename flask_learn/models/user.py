from flask_login import UserMixin
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import CreateUpdateAtMixin, CreateUpdateByMixin, UUIDMixin


class User(UUIDMixin, CreateUpdateAtMixin, CreateUpdateByMixin, UserMixin):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint('email', name="unique_user_email"),)

    username: Mapped[str] = mapped_column(String(128), nullable=False, comment="用户名")
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False, comment="密码")
    email: Mapped[str] = mapped_column(String(128), nullable=False, comment="邮箱")

    def get_id(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} email={self.email!r}>"
