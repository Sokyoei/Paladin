from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_babel import Babel
from flask_sqlalchemy.model import Model

from .config import settings
from .database import db_instance

db = db_instance.db


class AdminManager(object):

    def __init__(self):
        self.__admin: Admin | None = None
        self.__babel: Babel | None = None

    def init_app(self, app: Flask):
        self.__babel = Babel(app)
        self.__admin = Admin(app, name=settings.FLASK_ADMIN_NAME, theme=Bootstrap4Theme(swatch='minty'))

    @property
    def admin(self):
        if self.__admin is None:
            raise ValueError("Admin not initialized")
        return self.__admin

    @property
    def babel(self):
        if self.__babel is None:
            raise ValueError("Babel not initialized")
        return self.__babel

    def register_models(self, model_list: list[Model]):
        self.__admin.add_views(
            *[ModelView(model, db.session, endpoint=f"{model.__name__}_admin") for model in model_list]
        )


admin_manager = AdminManager()
