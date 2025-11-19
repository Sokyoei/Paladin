import uuid

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.crud import GenshinRoleCRUD
from fastapi_learn.schemas import GenshinRoleCreate, GenshinRoleResponse, GenshinRoleUpdate, Response

genshin_router = APIRouter(prefix="/genshin", tags=["原神"])


@genshin_router.post("/role/create", summary="新建角色", response_model=Response[GenshinRoleResponse])
async def create_genshin_role(role: GenshinRoleCreate, db: Session = Depends(get_db)):
    new_role = await GenshinRoleCRUD.create(db, role)
    return Response.success(new_role)


@genshin_router.delete(
    "/role/delete/{role_id}", summary="删除角色", response_model=Response[GenshinRoleResponse | None]
)
async def delete_genshin_role(role_id: uuid.UUID = Path(..., description="角色 UUID"), db: Session = Depends(get_db)):
    result = await GenshinRoleCRUD.delete(db, role_id)
    if result:
        return Response.success(result)
    return Response.fail("角色不存在")


@genshin_router.patch("/role/update/{role_id}", summary="更新角色", response_model=Response[GenshinRoleResponse | None])
async def update_genshin_role(
    role_id: uuid.UUID = Path(..., description="角色 UUID"),
    role_update: GenshinRoleUpdate = ...,
    db: Session = Depends(get_db),
):
    updated_role = await GenshinRoleCRUD.update(db, role_id, role_update)
    if updated_role:
        return Response.success(updated_role)
    return Response.fail("角色不存在")


@genshin_router.get("/role/search/{role_id}", summary="查找角色", response_model=Response[GenshinRoleResponse | None])
async def search_genshin_role(role_id: uuid.UUID = Path(..., description="角色 UUID"), db: Session = Depends(get_db)):
    role = await GenshinRoleCRUD.search(db, role_id)
    if role:
        return Response.success(role)
    return Response.fail("角色不存在")
