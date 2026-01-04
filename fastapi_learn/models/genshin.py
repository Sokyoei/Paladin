from datetime import date

from sqlalchemy import Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_learn.enums import GenshinElement, GenshinRoleQuality

from .base import CreateUpdateAtMixin, UUIDMixin


class GenshinRole(UUIDMixin, CreateUpdateAtMixin):
    __tablename__ = "genshin_role"
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="角色名")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="称号")
    quality: Mapped[GenshinRoleQuality] = mapped_column(Enum(GenshinRoleQuality), nullable=False, comment="星级")
    birthday: Mapped[date] = mapped_column(Date(), nullable=False, comment="出生日期")
    release_version: Mapped[str] = mapped_column(String(200), nullable=False, comment="上线版本")
    element: Mapped[GenshinElement] = mapped_column(Enum(GenshinElement), nullable=False, comment="元素")
    constellation: Mapped[str] = mapped_column(String(200), nullable=False, comment="命之座")
    affiliation: Mapped[str] = mapped_column(String(200), nullable=False, comment="所属阵营")
    special_dish: Mapped[str] = mapped_column(String(200), nullable=False, comment="特色菜肴")
