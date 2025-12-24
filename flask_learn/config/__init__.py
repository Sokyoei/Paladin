from .admin_manager import admin_manager
from .config import DEBUG, FIRST_UID, SECRET_KEY, SQLALCHEMY_DATABASE_URI, get_settings, settings
from .database import db_instance
from .debugger import debugger
from .login_manager import login_manager

__all__ = [
    "DEBUG",
    "FIRST_UID",
    "SECRET_KEY",
    "SQLALCHEMY_DATABASE_URI",
    "admin_manager",
    "db_instance",
    "debugger",
    "get_settings",
    "login_manager",
    "settings",
]
