from .music import bp as music_bp
from .user import bp as user_bp

all_blueprints = [
    # add your blueprints here
    user_bp,
    music_bp,
]

__all__ = ['all_blueprints']
