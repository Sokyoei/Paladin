from pydantic import BaseModel, Field

from flask_learn.enums.music import MusicType

from .base import CreateUpdateAtSchema, CreateUpdateBySchema, UUIDSchema


class MusicCreate(BaseModel):
    title: str = Field(..., description="歌曲名")
    artist: str = Field(..., description="歌手")
    album: str | None = Field(None, description="专辑")
    duration: float | None = Field(None, description="时长，单位秒")
    genre: MusicType = Field(MusicType.UNKNOW, description="曲风")


class MusicResponse(UUIDSchema, CreateUpdateAtSchema, CreateUpdateBySchema, MusicCreate):
    pass


class MusicUpdate(MusicCreate):
    title: str | None = Field(None)
    artist: str | None = Field(None)
    album: str | None = Field(None)
    duration: float | None = Field(None)
    genre: MusicType | None = Field(None)
