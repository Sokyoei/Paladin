import uuid

from flask import Blueprint

from flask_learn.crud import MusicCRUD
from flask_learn.schemas import MusicCreate, MusicUpdate
from flask_learn.utils import ApiResponse

bp = Blueprint("music", __name__, url_prefix="/music")


@bp.post("/")
async def create_music(music: MusicCreate):
    music = MusicCRUD.create(music)
    if music:
        return ApiResponse.success(music)
    return ApiResponse.error("创建失败")


@bp.get("/")
async def get_all_music():
    musics = MusicCRUD.get_all()
    if musics:
        return ApiResponse.success(musics)
    return ApiResponse.error("获取失败")


@bp.get("/<uuid:id>")
async def get_music(id: uuid.UUID):
    music = MusicCRUD.get(id)
    if music:
        return ApiResponse.success(music)
    return ApiResponse.error("获取失败")


@bp.put("/<uuid:id>")
async def update_music(id: uuid.UUID, music: MusicUpdate):
    music = MusicCRUD.update(id, music)
    if music:
        return ApiResponse.success(music)
    return ApiResponse.error("更新失败")


@bp.delete("/<uuid:id>")
async def delete_music(id: uuid.UUID):
    result = MusicCRUD.delete(id)
    if result:
        return ApiResponse.success()
    return ApiResponse.error("删除失败")
