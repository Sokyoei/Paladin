from uuid import UUID

from flask_learning.config import login_manager
from flask_learning.crud import UserCRUD


@login_manager.user_loader
def load_user(user_id):
    try:
        return UserCRUD.get(UUID(user_id), orm=True)
    except (ValueError, TypeError):
        return None
