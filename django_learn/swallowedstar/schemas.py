import uuid
from typing import Annotated

from ninja import Schema
from pydantic import Field

from .enums import SSElement, SSRealm

SwallowedStarRole_id = Annotated[uuid.UUID, Field(description="角色 UUID")]
SwallowedStarRole_name = Annotated[str, Field(description="角色名称", max_length=100)]
SwallowedStarRole_title = Annotated[str, Field(description="角色称号", max_length=255)]
SwallowedStarRole_realm = Annotated[SSRealm, Field(description="角色境界")]
SwallowedStarRole_element = Annotated[SSElement, Field(description="元素")]


class SwallowedStarRoleCreate(Schema):
    name: SwallowedStarRole_name
    title: SwallowedStarRole_title | None = None
    realm: SwallowedStarRole_realm
    element: SwallowedStarRole_element | None = None


class SwallowedStarRoleResponse(SwallowedStarRoleCreate):
    id: SwallowedStarRole_id


class SwallowedStarRoleUpdate(Schema):
    name: SwallowedStarRole_name | None = None
    title: SwallowedStarRole_title | None = None
    realm: SwallowedStarRole_realm | None = None
    element: SwallowedStarRole_element | None = None
