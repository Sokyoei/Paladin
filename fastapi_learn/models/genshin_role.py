import uuid
from datetime import date

from sqlalchemy import UUID, Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_learn.enums import GenshinRoleElement, GenshinRoleQuality

from .base import Base


class GenshinRole(Base):
    __tablename__ = "genshin_roles"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    quality: Mapped[GenshinRoleQuality] = mapped_column(Enum(GenshinRoleQuality), nullable=False)
    birthday: Mapped[date] = mapped_column(Date(), nullable=False)
    release_version: Mapped[str] = mapped_column(String(200), nullable=False)
    element: Mapped[GenshinRoleElement] = mapped_column(Enum(GenshinRoleElement), nullable=False)
    constellation: Mapped[str] = mapped_column(String(200), nullable=False)
    affiliation: Mapped[str] = mapped_column(String(200), nullable=False)
    special_dish: Mapped[str] = mapped_column(String(200), nullable=False)
