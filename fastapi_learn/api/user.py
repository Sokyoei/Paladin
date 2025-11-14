from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.crud import UserCRUD
from fastapi_learn.schemas import Response, UserCreate, UserResponse, UserUpdate

user_router = APIRouter(prefix="/user", tags=["用户"])


@user_router.put("/create", summary="新建用户", response_model=Response[UserResponse])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = await UserCRUD.create(db, user)
    return Response.success(new_user)


@user_router.delete("/delete", summary="删除用户")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = await UserCRUD.delete(db, user_id)
    return Response.success(result)


@user_router.post("/update", summary="更新用户信息", response_model=Response[UserResponse])
async def update_user(user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = await UserCRUD.update(db, user.id, user)
    return Response.success(updated_user)


@user_router.get("/search", summary="查找用户", response_model=Response[UserResponse])
async def search_user(user_id: int, db: Session = Depends(get_db)):
    user = await UserCRUD.search(db, user_id)
    return Response.success(user)
