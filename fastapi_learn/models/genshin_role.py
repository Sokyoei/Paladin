from datetime import date

from sqlalchemy import Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_learn.enums import GenshinRoleAttribute, GenshinRoleLevel

from .base import Base


class GenshinRole(Base):
    __tablename__ = "genshin_roles"
    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[GenshinRoleLevel] = mapped_column(Enum(GenshinRoleLevel), nullable=False)
    birthday: Mapped[date] = mapped_column(Date(), nullable=False)
    release_version: Mapped[str] = mapped_column(String(200), nullable=False)
    attribute: Mapped[GenshinRoleAttribute] = mapped_column(Enum(GenshinRoleAttribute), nullable=False)
    constellation: Mapped[str] = mapped_column(String(200), nullable=False)
    affiliation: Mapped[str] = mapped_column(String(200), nullable=False)
    special_dish: Mapped[str] = mapped_column(String(200), nullable=False)
