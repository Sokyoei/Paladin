from datetime import date

from sqlalchemy import Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_learn.enums import GenshinElement, GenshinRoleQuality

from .base import CreateUpdateAtMixin, UUIDMixin


class GenshinRole(UUIDMixin, CreateUpdateAtMixin):
    __tablename__ = "genshin_role"
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    quality: Mapped[GenshinRoleQuality] = mapped_column(Enum(GenshinRoleQuality), nullable=False)
    birthday: Mapped[date] = mapped_column(Date(), nullable=False)
    release_version: Mapped[str] = mapped_column(String(200), nullable=False)
    element: Mapped[GenshinElement] = mapped_column(Enum(GenshinElement), nullable=False)
    constellation: Mapped[str] = mapped_column(String(200), nullable=False)
    affiliation: Mapped[str] = mapped_column(String(200), nullable=False)
    special_dish: Mapped[str] = mapped_column(String(200), nullable=False)
