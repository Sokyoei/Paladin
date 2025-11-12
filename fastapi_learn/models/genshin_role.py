import enum
from datetime import date

from sqlalchemy import Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GenshinRoleLevel(enum.IntEnum):
    four = 4
    five = 5


class GenshinRole(Base):
    __tablename__ = "genshin_roles"
    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    level: Mapped[GenshinRoleLevel] = mapped_column(Enum(GenshinRoleLevel))
    birthday: Mapped[date] = mapped_column(Date())
