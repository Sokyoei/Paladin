from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.crud import UserCRUD
from fastapi_learn.schemas import User

user_router = APIRouter(prefix="/user", tags=["用户"])


@user_router.put("/user", summary="新建用户")
async def create_user(user: User, db: Session = Depends(get_db)):
    return UserCRUD.create()


@user_router.delete("/user/{user_id}", summary="删除用户")
async def delete_user():
    pass


@user_router.post("/user/{user_id}", summary="更新用户信息")
async def update_user():
    pass


@user_router.get("/user/{user_id}", summary="查找用户")
async def search_user():
    pass
