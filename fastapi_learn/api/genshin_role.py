from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.schemas import GenshinRole

router = APIRouter(tags=["原神角色"])


@router.put("/genshin_role", summary="新建角色")
async def create_genshin_role(role: GenshinRole, db: Session = Depends(get_db)):
    pass


@router.delete("/genshin_role/{role_name}", summary="删除角色")
async def delete_genshin_role():
    pass


@router.post("/genshin_role/{role_name}", summary="更新角色")
async def update_genshin_role():
    pass


@router.get("/genshin_role/{role_name}", summary="查找角色")
async def search_genshin_role():
    pass
