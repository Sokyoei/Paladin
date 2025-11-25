import uuid
from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learn.config import get_db
from fastapi_learn.crud import GenshinRoleCRUD
from fastapi_learn.schemas import GenshinRoleCreate, GenshinRoleResponse, GenshinRoleUpdate
from fastapi_learn.utils import ApiResponse

genshin_role_router = APIRouter(prefix="/genshin/roles", tags=["原神角色"])


@genshin_role_router.post("", summary="新建角色", response_model=ApiResponse[GenshinRoleResponse])
async def create_genshin_role(
    role: Annotated[GenshinRoleCreate, Body(description="角色信息")], db: AsyncSession = Depends(get_db)
):
    new_role = await GenshinRoleCRUD.create(db, role)
    return ApiResponse.success(new_role)


@genshin_role_router.delete("/{role_id}", summary="删除角色", response_model=ApiResponse[GenshinRoleResponse | None])
async def delete_genshin_role(
    role_id: Annotated[uuid.UUID, Path(description="角色 UUID")], db: AsyncSession = Depends(get_db)
):
    result = await GenshinRoleCRUD.delete(db, role_id)
    if result:
        return ApiResponse.success(result)
    return ApiResponse.fail("角色不存在")


@genshin_role_router.patch("/{role_id}", summary="更新角色", response_model=ApiResponse[GenshinRoleResponse | None])
async def update_genshin_role(
    role_id: Annotated[uuid.UUID, Path(description="角色 UUID")],
    role_update: Annotated[GenshinRoleUpdate, Body(description="角色更新信息")],
    db: AsyncSession = Depends(get_db),
):
    updated_role = await GenshinRoleCRUD.update(db, role_id, role_update)
    if updated_role:
        return ApiResponse.success(updated_role)
    return ApiResponse.fail("角色不存在")


@genshin_role_router.get("/{role_id}", summary="查找角色", response_model=ApiResponse[GenshinRoleResponse | None])
async def search_genshin_role(
    role_id: Annotated[uuid.UUID, Path(description="角色 UUID")], db: AsyncSession = Depends(get_db)
):
    role = await GenshinRoleCRUD.search(db, role_id)
    if role:
        return ApiResponse.success(role)
    return ApiResponse.fail("角色不存在")


@genshin_role_router.get("", summary="获取所有角色", response_model=ApiResponse[List[GenshinRoleResponse]])
async def get_all_roles(db: AsyncSession = Depends(get_db)):
    roles = await GenshinRoleCRUD.get_all(db)
    return ApiResponse.success(roles)
