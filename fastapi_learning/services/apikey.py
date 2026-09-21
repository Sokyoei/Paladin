from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning.config import get_db
from fastapi_learning.crud import APIKeyCRUD

api_key_header = APIKeyHeader(name="Ahri-API-Key", description="Requires Ahri-API-Key header", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header), db: AsyncSession = Depends(get_db)):  # noqa: B008
    if not api_key or not await APIKeyCRUD.count(db, key=api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")
    return api_key
