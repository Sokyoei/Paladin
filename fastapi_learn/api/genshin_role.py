from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.crud import GenshinRoleCRUD
from fastapi_learn.schemas import GenshinRole, Response

genshin_role_router = APIRouter(prefix="/genshin_role", tags=["原神角色"])


@genshin_role_router.put("/create", summary="新建角色", response_model=Response[GenshinRole])
async def create_genshin_role(role: GenshinRole, db: Session = Depends(get_db)):
    await GenshinRoleCRUD.create(db, role)
    return Response.success(role)


@genshin_role_router.delete("/delete", summary="删除角色")
async def delete_genshin_role(role_id: int, db: Session = Depends(get_db)):
    await GenshinRoleCRUD.delete(db, role_id)
    return Response.success()


@genshin_role_router.post("/update", summary="更新角色")
async def update_genshin_role(role: GenshinRole, db: Session = Depends(get_db)):
    await GenshinRoleCRUD.update(db, role.id, role)
    return Response.success()


@genshin_role_router.get("/search", summary="查找角色")
async def search_genshin_role(role_id: int, db: Session = Depends(get_db)):
    role = await GenshinRoleCRUD.search(db, role_id)
    return Response.success(role)
