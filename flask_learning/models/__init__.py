from .music import Music
from .user import User

all_models = [
    # add your models here, for registering in flask-admin
    Music,
    User,
]

__all__ = ["Music", "User", "all_models"]
