from fastapi_learn.models import GenshinRole
from fastapi_learn.schemas import GenshinRoleCreate, GenshinRoleResponse, GenshinRoleUpdate

from .base import BaseAsyncCRUD


class GenshinRoleCRUD(BaseAsyncCRUD[GenshinRole, GenshinRoleCreate, GenshinRoleUpdate, GenshinRoleResponse]):

    model = GenshinRole
    schema = GenshinRoleResponse
