from .apikey import apikey_router
from .genshin import genshin_role_router
from .user import user_router

all_routers = [
    # add your routers here
    genshin_role_router,
    user_router,
    apikey_router,
]

__all__ = ["all_routers"]
