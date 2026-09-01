import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning.config import get_db
from fastapi_learning.crud import UserCRUD
from fastapi_learning.schemas import UserCreate, UserResponse, UserUpdate
from fastapi_learning.utils import ApiResponse

user_router = APIRouter(prefix="/users", tags=["用户"])


@user_router.post("", summary="新建用户", response_model=ApiResponse[UserResponse | None])
async def create_user(
    user: Annotated[UserCreate, Body(description="用户信息")], db: Annotated[AsyncSession, Depends(get_db)]
):
    new_user = await UserCRUD.create(db, user)
    if new_user:
        return ApiResponse.success(new_user)
    return ApiResponse.error("用户创建失败")


@user_router.delete("/{user_id}", summary="删除用户", response_model=ApiResponse[UserResponse | None])
async def delete_user(
    user_id: Annotated[uuid.UUID, Path(description="角色 UUID")], db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await UserCRUD.delete(db, user_id)
    if result:
        return ApiResponse.success(result)
    return ApiResponse.error("用户不存在")


@user_router.patch("/{user_id}", summary="更新用户", response_model=ApiResponse[UserResponse | None])
async def update_user(
    user_id: Annotated[uuid.UUID, Path(description="角色 UUID")],
    user_update: Annotated[UserUpdate, Body(description="用户更新信息")],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    updated_user = await UserCRUD.update(db, user_id, user_update)
    if updated_user:
        return ApiResponse.success(updated_user)
    return ApiResponse.error("用户不存在")


@user_router.get("/{user_id}", summary="查找用户", response_model=ApiResponse[UserResponse | None])
async def search_user(
    user_id: Annotated[uuid.UUID, Path(description="角色 UUID")], db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await UserCRUD.search(db, user_id)
    if user:
        return ApiResponse.success(user)
    return ApiResponse.error("用户不存在")


@user_router.get("", summary="获取所有用户", response_model=ApiResponse[list[UserResponse]])
async def get_all_users(db: Annotated[AsyncSession, Depends(get_db)]):
    users = await UserCRUD.get_all(db)
    return ApiResponse.success(users)
