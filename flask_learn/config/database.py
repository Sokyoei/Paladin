from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class Database(object):

    def __init__(self):
        self.__db = SQLAlchemy()
        self.__migrate = Migrate()

    def init_app(self, app: Flask):
        self.__db.init_app(app)
        self.__migrate.init_app(app, self.__db)

    @property
    def db(self) -> SQLAlchemy:
        return self.__db

    @property
    def migrate(self) -> Migrate:
        return self.__migrate

    def init_db(self, app: Flask):
        with app.app_context():
            self.__db.create_all()

    def close_db(self, app: Flask):
        with app.app_context():
            self.__db.engine.dispose()


db_instance = Database()
