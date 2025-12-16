from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CreateUpdateAtSchema(BaseModel):
    created_at: datetime = Field(description="Created at")
    updated_at: datetime = Field(description="Updated at")


class UUIDSchema(BaseModel):
    id: uuid.UUID = Field(description="Unique identifier")


class CreateUpdateBySchema(BaseModel):
    created_by: uuid.UUID = Field(description="Created by")
    updated_by: uuid.UUID = Field(description="Updated by")
