import uuid
from datetime import date
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from fastapi_learn.enums import GenshinRoleElement, GenshinRoleQuality

GenshineRole_id = Annotated[uuid.UUID, Field(description="角色 UUID")]
GenshineRole_name = Annotated[str, Field(description="角色名称", max_length=255)]
GenshineRole_title = Annotated[str, Field(description="角色称号", max_length=255)]
GenshineRole_quality = Annotated[GenshinRoleQuality, Field(description="角色星级")]
GenshineRole_birthday = Annotated[date, Field(description="出生日期")]
GenshineRole_release_version = Annotated[str, Field(description="上线版本", max_length=200)]
GenshineRole_element = Annotated[GenshinRoleElement, Field(description="元素(风/水/火/冰/雷/岩/草)")]
GenshineRole_constellation = Annotated[str, Field(description="命之座", max_length=200)]
GenshineRole_affiliation = Annotated[str, Field(description="所属势力", max_length=200)]
GenshineRole_special_dish = Annotated[str, Field(description="特色菜", max_length=200)]


class GenshinRoleCreate(BaseModel):
    name: GenshineRole_name
    title: GenshineRole_title
    quality: GenshineRole_quality
    birthday: GenshineRole_birthday
    release_version: GenshineRole_release_version
    element: GenshineRole_element
    constellation: GenshineRole_constellation
    affiliation: GenshineRole_affiliation
    special_dish: GenshineRole_special_dish


class GenshinRoleResponse(GenshinRoleCreate):
    id: GenshineRole_id


class GenshinRoleUpdate(BaseModel):
    id: GenshineRole_id
    name: Optional[GenshineRole_name]
    title: Optional[GenshineRole_title]
    quality: Optional[GenshineRole_quality]
    birthday: Optional[GenshineRole_birthday]
    release_version: Optional[GenshineRole_release_version]
    element: Optional[GenshineRole_element]
    constellation: Optional[GenshineRole_constellation]
    affiliation: Optional[GenshineRole_affiliation]
    special_dish: Optional[GenshineRole_special_dish]
