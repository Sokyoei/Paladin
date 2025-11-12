from fastapi_learn.models import User
from fastapi_learn.schemas import User as UserSchema

from .base import BaseCRUD


class UserCRUD(BaseCRUD[User, UserSchema]):

    model = User
    schema = UserSchema
