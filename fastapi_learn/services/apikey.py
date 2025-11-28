from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learn.config import get_db
from fastapi_learn.crud import APIKeyCRUD

api_key_header = APIKeyHeader(name="Ahri-API-Key", description="Requires Ahri-API-Key header", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header), db: AsyncSession = Depends(get_db)):
    apikeys = await APIKeyCRUD.get_all(db)
    valid_api_keys = {apikey.key for apikey in apikeys}
    if not api_key or api_key not in valid_api_keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")
    return api_key
