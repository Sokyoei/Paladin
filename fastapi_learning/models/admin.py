"""
注册到 sqladmin 后台管理
"""

from sqladmin import ModelView

from .genshin import GenshinRole
from .user import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]  # noqa: RUF012


class GenshinRoleAdmin(ModelView, model=GenshinRole):
    column_list = [GenshinRole.id, GenshinRole.name]  # noqa: RUF012


all_model_views: list[type[ModelView]] = [UserAdmin, GenshinRoleAdmin]
