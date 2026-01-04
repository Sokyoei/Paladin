from sqlalchemy import Enum, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from flask_learn.enums import MusicLoaction, MusicType

from .base import CreateUpdateAtMixin, CreateUpdateByMixin, UUIDMixin


class Music(UUIDMixin, CreateUpdateAtMixin, CreateUpdateByMixin):
    __tablename__ = "music"

    title: Mapped[str] = mapped_column(String(128), nullable=False, comment="音乐标题")
    artist: Mapped[str] = mapped_column(String(128), nullable=False, comment="艺术家")
    album: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="专辑")
    duration: Mapped[float | None] = mapped_column(Float, nullable=True, comment="时长")
    genre: Mapped[MusicType] = mapped_column(Enum(MusicType), default=MusicType.UNKNOW, nullable=False, comment="类型")
    location: Mapped[MusicLoaction] = mapped_column(Enum(MusicLoaction), nullable=False, comment="位置（网络/本地）")
    url: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="音乐地址")

    def __repr__(self) -> str:
        return f"<Music id={self.id} title={self.title!r} artist={self.artist!r}>"
