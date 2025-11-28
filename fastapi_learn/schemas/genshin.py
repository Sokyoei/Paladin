import uuid
from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field

from fastapi_learn.enums import GenshinElement, GenshinRoleQuality

GenshinRole_id = Annotated[uuid.UUID, Field(description="角色 UUID")]
GenshinRole_name = Annotated[str, Field(description="角色名称", max_length=255)]
GenshinRole_title = Annotated[str, Field(description="角色称号", max_length=255)]
GenshinRole_quality = Annotated[GenshinRoleQuality, Field(description="角色星级")]
GenshinRole_birthday = Annotated[date, Field(description="出生日期")]
GenshinRole_release_version = Annotated[str, Field(description="上线版本", max_length=200)]
GenshinRole_element = Annotated[GenshinElement, Field(description="元素(风/水/火/冰/雷/岩/草)")]
GenshinRole_constellation = Annotated[str, Field(description="命之座", max_length=200)]
GenshinRole_affiliation = Annotated[str, Field(description="所属势力", max_length=200)]
GenshinRole_special_dish = Annotated[str, Field(description="特色菜", max_length=200)]


class GenshinRoleCreate(BaseModel):
    name: GenshinRole_name
    title: GenshinRole_title
    quality: GenshinRole_quality
    birthday: GenshinRole_birthday
    release_version: GenshinRole_release_version
    element: GenshinRole_element
    constellation: GenshinRole_constellation
    affiliation: GenshinRole_affiliation
    special_dish: GenshinRole_special_dish


class GenshinRoleResponse(GenshinRoleCreate):
    id: GenshinRole_id


class GenshinRoleUpdate(BaseModel):
    name: GenshinRole_name | None = None
    title: GenshinRole_title | None = None
    quality: GenshinRole_quality | None = None
    birthday: GenshinRole_birthday | None = None
    release_version: GenshinRole_release_version | None = None
    element: GenshinRole_element | None = None
    constellation: GenshinRole_constellation | None = None
    affiliation: GenshinRole_affiliation | None = None
    special_dish: GenshinRole_special_dish | None = None
