import asyncio
import base64
import secrets
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning.models import APIKey
from fastapi_learning.schemas import APIKeyCreate, APIKeyResponse, APIKeyUpdate

from .base import BaseAsyncCRUD


class APIKeyCRUD(BaseAsyncCRUD[APIKey, APIKeyCreate, APIKeyUpdate, APIKeyResponse]):
    model = APIKey
    schema = APIKeyResponse

    @classmethod
    async def create(cls, db: AsyncSession, data: APIKeyCreate) -> APIKeyResponse:
        new_key = await asyncio.to_thread(generate_api_key)
        db_obj = cls.model(key=new_key, **data.model_dump(exclude_none=True, exclude_unset=True, exclude={"key"}))
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    async def search_by_user_id(cls, db: AsyncSession, user_id: uuid.UUID) -> list[APIKeyResponse]:
        return await cls.get_all(db, user_id=user_id)

    @classmethod
    async def delete_by_key(cls, db: AsyncSession, key: str) -> APIKeyResponse | None:
        objs = await cls.get_all(db, key=key)
        if not objs:
            return None
        return await cls.delete(db, objs[0].id)


def generate_api_key(prefix: str | None = "ahri_", random_bytes_length: int = 32) -> str:
    random_bytes = secrets.token_bytes(random_bytes_length)
    url_safe_b64 = base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")

    if prefix:
        return f"{prefix}{url_safe_b64}"
    return url_safe_b64
