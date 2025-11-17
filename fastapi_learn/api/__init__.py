from .genshin import genshin_router
from .user import user_router as user_router

all_routers = [
    # add your routers here
    genshin_router,
    user_router,
]

__all__ = ["all_routers"]
