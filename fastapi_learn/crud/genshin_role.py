from fastapi_learn.models import GenshinRole
from fastapi_learn.schemas import GenshinRole as GenshinRoleSchema

from .base import BaseCRUD


class GenshinRoleCRUD(BaseCRUD[GenshinRole, GenshinRoleSchema]):

    model = GenshinRole
    schema = GenshinRoleSchema
