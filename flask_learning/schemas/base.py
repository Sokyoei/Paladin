from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, create_model


class CreateUpdateAtSchema(BaseModel):
    created_at: datetime = Field(description="Created at")
    updated_at: datetime = Field(description="Updated at")


class UUIDSchema(BaseModel):
    id: uuid.UUID = Field(description="Unique identifier")


class CreateUpdateBySchema(BaseModel):
    created_by: uuid.UUID = Field(description="Created by")
    updated_by: uuid.UUID = Field(description="Updated by")


def make_fields_optional(
    model_cls: type[BaseModel], maked_model_name: str = f'{type.__name__}Optional'
) -> type[BaseModel]:
    """
    see https://docs.pydantic.dev/latest/examples/dynamic_models/
    """
    new_fields = {}

    for f_name, f_info in model_cls.model_fields.items():
        new_fields[f_name] = (
            Annotated[f_info.annotation | None, *f_info.metadata, Field(**f_info.asdict()['attributes'])],
            None,
        )
    f_info.asdict()["annotation"]
    return create_model(maked_model_name, __base__=model_cls, **new_fields)
