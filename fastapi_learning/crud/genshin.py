from fastapi_learning.models import GenshinRole
from fastapi_learning.schemas import GenshinRoleCreate, GenshinRoleResponse, GenshinRoleUpdate

from .base import BaseAsyncCRUD


class GenshinRoleCRUD(BaseAsyncCRUD[GenshinRole, GenshinRoleCreate, GenshinRoleUpdate, GenshinRoleResponse]):

    model = GenshinRole
    schema = GenshinRoleResponse
