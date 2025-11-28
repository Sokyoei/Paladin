import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CreateUpdateMixin(BaseModel):
    create_at: datetime = Field(description="Created at")
    update_at: datetime = Field(description="Updated at")


class UUIDMixin(BaseModel):
    id: uuid.UUID = Field(description="Unique identifier")
