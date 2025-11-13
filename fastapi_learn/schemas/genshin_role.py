from datetime import date

from pydantic import BaseModel, Field

from fastapi_learn.enums import GenshinRoleAttribute, GenshinRoleLevel


class GenshinRole(BaseModel):
    name: str = Field(description="角色名称", max_length=255)
    title: str = Field(description="角色称号", max_length=255)
    level: GenshinRoleLevel = Field(description="角色星级")
    birthday: date = Field(description="出生日期")
    release_version: str = Field(description="上线版本", max_length=200)
    attribute: GenshinRoleAttribute = Field(description="属性(风/水/火/冰/雷/岩/草)", max_length=200)
    constellation: str = Field(description="命之座", max_length=200)
    affiliation: str = Field(description="所属势力", max_length=200)
    special_dish: str = Field(description="特色菜", max_length=200)
