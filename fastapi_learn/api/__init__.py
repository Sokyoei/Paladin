from .genshin_role import router as genshin_role_router
from .item import router as item_router
from .user import router as user_router

all_routers = [
    # add your routers here
    genshin_role_router,
    item_router,
    user_router,
]

__all__ = ["all_routers"]
