import uuid

from flask import Blueprint

from flask_learn.crud import UserCRUD
from flask_learn.schemas import UserCreate, UserUpdate
from flask_learn.utils import ApiResponse

bp = Blueprint('user', __name__, url_prefix="/user")


@bp.post("/")
async def create_user(user: UserCreate):
    user = UserCRUD.create(user)
    if user:
        return ApiResponse.success(user)
    return ApiResponse.error("用户创建失败")


@bp.get("/")
async def get_all_user():
    users = UserCRUD.get_all()
    if users:
        return ApiResponse.success(users)
    return ApiResponse.error("用户不存在")


@bp.get("/<uuid:id>")
async def get_user(id: uuid.UUID):
    user = UserCRUD.get(id)
    if user:
        return ApiResponse.success(user)
    return ApiResponse.error("用户不存在")


@bp.put("/<uuid:id>")
async def update_user(id: uuid.UUID, user: UserUpdate):
    user = UserCRUD.update(id, user)
    if user:
        return ApiResponse.success(user)
    return ApiResponse.error("用户更新失败")


@bp.delete("/<uuid:id>")
async def delete_user(id: uuid.UUID):
    result = UserCRUD.delete(id)
    if result:
        return ApiResponse.success(result)
    return ApiResponse.error("用户删除失败")
