from datetime import date

from pydantic import BaseModel

from fastapi_learn.models.genshin_role import GenshinRoleLevel


class GenshinRole(BaseModel):
    name: str
    level: GenshinRoleLevel
    birthday: date
