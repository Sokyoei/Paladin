import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CreateUpdateAtSchema(BaseModel):
    created_at: datetime = Field(description="Created at")
    updated_at: datetime = Field(description="Updated at")


class UUIDSchema(BaseModel):
    id: uuid.UUID = Field(description="Unique identifier")
