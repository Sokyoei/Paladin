from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import settings


class Database(object):

    def __init__(self):
        self.__db = SQLAlchemy()
        self.__migrate = Migrate()

    def init_app(self, app: Flask):
        app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI

        self.__db.init_app(app)
        self.__migrate.init_app(app, self.__db)

    @property
    def db(self) -> SQLAlchemy:
        return self.__db

    @property
    def migrate(self) -> Migrate:
        return self.__migrate


db_instance = Database()
