import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning.config import get_db
from fastapi_learning.crud import APIKeyCRUD, UserCRUD
from fastapi_learning.schemas import APIKeyCreate, APIKeyResponse
from fastapi_learning.services.apikey import verify_api_key
from fastapi_learning.utils import ApiResponse

apikey_router = APIRouter(prefix="/apikey", tags=["API Key"])


@apikey_router.get("/protected", dependencies=[Security(verify_api_key)])
async def protected():
    return ApiResponse.success({"message": "访问成功！这是受 API 密钥保护的接口"})


@apikey_router.post("", response_model=ApiResponse[APIKeyResponse])
async def create_apikey(data: APIKeyCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    if not await UserCRUD.exists(db, data.user_id):
        raise HTTPException(status_code=404, detail="用户不存在")
    new_apikey = await APIKeyCRUD.create(db, data)
    return ApiResponse.success(new_apikey)


@apikey_router.get("/{user_id}", response_model=ApiResponse[list[APIKeyResponse]])
async def get_apikey_by_user_id(user_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    if not await UserCRUD.exists(db, user_id):
        raise HTTPException(status_code=404, detail="用户不存在")
    apikeys = await APIKeyCRUD.search_by_user_id(db, user_id)
    return ApiResponse.success(apikeys)


@apikey_router.delete("/{key}", response_model=ApiResponse[APIKeyResponse | None])
async def delete_apikey(key: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await APIKeyCRUD.delete_by_key(db, key)
    if result:
        return ApiResponse.success(result)
    raise HTTPException(status_code=404, detail="API 密钥不存在")
