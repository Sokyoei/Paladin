from sqlalchemy import Enum, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from flask_learn.enums.music import MusicType

from .base import CreateUpdateAtMixin, CreateUpdateByMixin, UUIDMixin


class Music(UUIDMixin, CreateUpdateAtMixin, CreateUpdateByMixin):
    __tablename__ = "music"

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    artist: Mapped[str] = mapped_column(String(128), nullable=False)
    album: Mapped[str | None] = mapped_column(String(128), nullable=True)
    duration: Mapped[float | None] = mapped_column(Float, nullable=True)
    genre: Mapped[MusicType] = mapped_column(Enum(MusicType), default=MusicType.OTHER, nullable=False)

    def __repr__(self) -> str:
        return f"<Music id={self.id} title={self.title!r} artist={self.artist!r}>"
