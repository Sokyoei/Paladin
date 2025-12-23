from .music import Music

all_models = [
    # add your models here, for registering in flask-admin
    Music
]

__all__ = ["Music", "all_models"]
