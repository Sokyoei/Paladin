import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning.config import get_db, settings
from fastapi_learning.crud import UserCRUD
from fastapi_learning.models import User
from fastapi_learning.schemas import UserCreate, UserResponse, UserUpdate
from fastapi_learning.services.user import auth_backend, current_active_user, fastapi_users, google_oauth_client
from fastapi_learning.utils import ApiResponse

if settings.USE_FASTAPI_USERS:
    user_router = APIRouter()

    user_router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["认证"])
    user_router.include_router(
        fastapi_users.get_register_router(UserResponse, UserCreate), prefix="/auth", tags=["认证"]
    )
    user_router.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["认证"])
    user_router.include_router(fastapi_users.get_verify_router(UserResponse), prefix="/auth", tags=["认证"])
    user_router.include_router(fastapi_users.get_users_router(UserResponse, UserUpdate), prefix="/users", tags=["用户"])
    user_router.include_router(
        fastapi_users.get_oauth_router(google_oauth_client, auth_backend, settings.JWT_SECRET_KEY),
        prefix="/auth/google",
        tags=["认证"],
    )

    @user_router.get("/authenticated-route")
    async def authenticated_route(user: Annotated[User, Depends(current_active_user)]):
        """访问受保护的接口"""
        return ApiResponse.success({"message": f"Hello {user.name}!"})

else:
    user_router = APIRouter(prefix="/users", tags=["用户"])

    @user_router.post("", summary="新建用户", response_model=ApiResponse[UserResponse | None])
    async def create_user(
        user: Annotated[UserCreate, Body(description="用户信息")], db: Annotated[AsyncSession, Depends(get_db)]
    ):
        new_user = await UserCRUD.create(db, user)
        if new_user:
            return ApiResponse.success(new_user)
        raise HTTPException(status_code=400, detail="用户创建失败")

    @user_router.delete("/{user_id}", summary="删除用户", response_model=ApiResponse[UserResponse | None])
    async def delete_user(
        user_id: Annotated[uuid.UUID, Path(description="角色 UUID")], db: Annotated[AsyncSession, Depends(get_db)]
    ):
        result = await UserCRUD.delete(db, user_id)
        if result:
            return ApiResponse.success(result)
        raise HTTPException(status_code=404, detail="用户不存在")

    @user_router.patch("/{user_id}", summary="更新用户", response_model=ApiResponse[UserResponse | None])
    async def update_user(
        user_id: Annotated[uuid.UUID, Path(description="角色 UUID")],
        user_update: Annotated[UserUpdate, Body(description="用户更新信息")],
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        updated_user = await UserCRUD.update(db, user_id, user_update)
        if updated_user:
            return ApiResponse.success(updated_user)
        raise HTTPException(status_code=404, detail="用户不存在")

    @user_router.get("/{user_id}", summary="查找用户", response_model=ApiResponse[UserResponse | None])
    async def search_user(
        user_id: Annotated[uuid.UUID, Path(description="角色 UUID")], db: Annotated[AsyncSession, Depends(get_db)]
    ):
        user = await UserCRUD.search(db, user_id)
        if user:
            return ApiResponse.success(user)
        raise HTTPException(status_code=404, detail="用户不存在")

    @user_router.get("", summary="获取所有用户", response_model=ApiResponse[list[UserResponse]])
    async def get_all_users(db: Annotated[AsyncSession, Depends(get_db)]):
        users = await UserCRUD.get_all(db)
        return ApiResponse.success(users)
