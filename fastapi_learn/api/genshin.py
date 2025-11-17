import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.crud import GenshinRoleCRUD
from fastapi_learn.schemas import GenshinRoleCreate, GenshinRoleResponse, GenshinRoleUpdate, Response

genshin_router = APIRouter(prefix="/genshin_role", tags=["原神角色"])


@genshin_router.put("/create", summary="新建角色", response_model=Response[GenshinRoleResponse])
async def create_genshin_role(role: GenshinRoleCreate, db: Session = Depends(get_db)):
    new_role = await GenshinRoleCRUD.create(db, role)
    return Response.success(new_role)


@genshin_router.delete("/delete", summary="删除角色")
async def delete_genshin_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    result = await GenshinRoleCRUD.delete(db, role_id)
    return Response.success(result)


@genshin_router.post("/update", summary="更新角色", response_model=Response[GenshinRoleResponse])
async def update_genshin_role(role: GenshinRoleUpdate, db: Session = Depends(get_db)):
    updated_role = await GenshinRoleCRUD.update(db, role.id, role)
    return Response.success(updated_role)


@genshin_router.get("/search", summary="查找角色", response_model=Response[GenshinRoleResponse])
async def search_genshin_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    role = await GenshinRoleCRUD.search(db, role_id)
    return Response.success(role)
