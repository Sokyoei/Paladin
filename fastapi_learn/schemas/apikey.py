import uuid

from pydantic import BaseModel, Field

from .base import CreateUpdateMixin, UUIDMixin


class APIKeyCreate(BaseModel):
    user_id: uuid.UUID = Field(description="User ID")


class APIKeyResponse(APIKeyCreate, CreateUpdateMixin, UUIDMixin):
    id: uuid.UUID = Field(description="API key ID")
    key: str = Field(description="API key", max_length=255)


class APIKeyUpdate(APIKeyCreate):
    pass
