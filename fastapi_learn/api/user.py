from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.crud import UserCRUD
from fastapi_learn.schema import User

router = APIRouter(tags=["用户"])


@router.put("/users", summary="新建用户")
async def create_user(user: User, db: Session = Depends(get_db)):
    return UserCRUD.create_user()


@router.delete("/users/{user_id}", summary="删除用户")
async def delete_user():
    pass


@router.post("/users/{user_id}", summary="更新用户信息")
async def update_user():
    pass


@router.get("/users/{user_id}", summary="查找用户")
async def search_user():
    pass
