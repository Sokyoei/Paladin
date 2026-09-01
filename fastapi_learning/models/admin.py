"""
注册到 sqladmin 后台管理
"""

from typing import ClassVar, TypeVar

from sqladmin import ModelView
from sqlalchemy import Column
from sqlalchemy.orm import MappedColumn

from .genshin import GenshinRole
from .user import User

MV = TypeVar("MV", bound=ModelView)


class UserAdmin(ModelView, model=User):
    column_list: ClassVar[list[Column | MappedColumn]] = [User.id, User.email]


class GenshinRoleAdmin(ModelView, model=GenshinRole):
    column_list: ClassVar[list[Column | MappedColumn]] = [GenshinRole.id, GenshinRole.name]


all_model_views: list[type[MV]] = [UserAdmin, GenshinRoleAdmin]
