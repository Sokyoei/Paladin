from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.crud import UserCRUD
from fastapi_learn.schemas import Response, User

user_router = APIRouter(prefix="/user", tags=["用户"])


@user_router.put("/create", summary="新建用户", response_model=Response[User])
async def create_user(user: User, db: Session = Depends(get_db)):
    await UserCRUD.create(db, user)
    return Response.success(user)


@user_router.delete("/delete", summary="删除用户")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    await UserCRUD.delete(db, user_id)
    return Response.success()


@user_router.post("/update", summary="更新用户信息")
async def update_user(user: User, db: Session = Depends(get_db)):
    await UserCRUD.update(db, user.id, user)
    return Response.success()


@user_router.get("/search", summary="查找用户")
async def search_user(user_id: int, db: Session = Depends(get_db)):
    await UserCRUD.search(db, user_id)
    return Response.success()
