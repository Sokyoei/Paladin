import uuid

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from fastapi_learn.config import get_db
from fastapi_learn.crud import UserCRUD
from fastapi_learn.schemas import Response, UserCreate, UserResponse, UserUpdate

user_router = APIRouter(prefix="/user", tags=["用户"])


@user_router.post("/create", summary="新建用户", response_model=Response[UserResponse])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = await UserCRUD.create(db, user)
    return Response.success(new_user)


@user_router.delete("/delete/{user_id}", summary="删除用户", response_model=Response[UserResponse | None])
async def delete_user(user_id: uuid.UUID = Path(..., description="角色 UUID"), db: Session = Depends(get_db)):
    result = await UserCRUD.delete(db, user_id)
    if result:
        return Response.success(result)
    return Response.fail("用户不存在")


@user_router.patch("/update/{user_id}", summary="更新用户", response_model=Response[UserResponse | None])
async def update_user(
    user_id: uuid.UUID = Path(..., description="角色 UUID"),
    user_update: UserUpdate = ...,
    db: Session = Depends(get_db),
):
    updated_user = await UserCRUD.update(db, user_id, user_update)
    if updated_user:
        return Response.success(updated_user)
    return Response.fail("用户不存在")


@user_router.get("/search/{user_id}", summary="查找用户", response_model=Response[UserResponse | None])
async def search_user(user_id: uuid.UUID = Path(..., description="角色 UUID"), db: Session = Depends(get_db)):
    user = await UserCRUD.search(db, user_id)
    if user:
        return Response.success(user)
    return Response.fail("用户不存在")
