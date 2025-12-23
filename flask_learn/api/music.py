import uuid

from flask import Blueprint

from flask_learn.crud import MusicCRUD
from flask_learn.schemas import MusicCreate, MusicResponse, MusicUpdate

bp = Blueprint("music", __name__, url_prefix="/music")


@bp.post("/")
async def create_music(music: MusicCreate):
    music = MusicCRUD.create(music)
    return MusicResponse.model_validate(music, from_attributes=True)


@bp.get("/")
async def get_all_music():
    musics = MusicCRUD.get_all()
    return [MusicResponse.model_validate(music, from_attributes=True) for music in musics]


@bp.get("/<id>")
async def get_music(id: uuid.UUID):
    music = MusicCRUD.get(id)
    return MusicResponse.model_validate(music, from_attributes=True)


@bp.put("/<id>")
async def update_music(id: uuid.UUID, music: MusicUpdate):
    music = MusicCRUD.update(id, music)
    return MusicResponse.model_validate(music, from_attributes=True)


@bp.delete("/<id>")
async def delete_music(id: uuid.UUID):
    return MusicCRUD.delete(id)
