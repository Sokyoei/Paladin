from sqladmin import Admin
from starlette.applications import Starlette

from fastapi_learn.models import all_model_views

from .database import db_instance


class AdminManager(object):

    def __init__(self):
        self.__admin: Admin | None = None

    def init_app(self, app: Starlette) -> None:
        self.__admin = Admin(app, db_instance.engine)
        app.state.admin = self.__admin

    @property
    def admin(self) -> Admin:
        if not self.__admin:
            raise ValueError("Admin not initialized")
        return self.__admin

    def register_models(self) -> None:
        for model in all_model_views:
            self.__admin.add_view(model)


admin_manager = AdminManager()
