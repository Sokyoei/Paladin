import uuid

from pydantic import BaseModel, Field

from .base import CreateUpdateAtSchema, UUIDSchema


class APIKeyCreate(BaseModel):
    user_id: uuid.UUID = Field(description="User ID")


class APIKeyResponse(APIKeyCreate, CreateUpdateAtSchema, UUIDSchema):
    key: str = Field(description="API key", max_length=255)


class APIKeyUpdate(APIKeyCreate):
    pass
