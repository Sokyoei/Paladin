from fastapi_learn.models import User
from fastapi_learn.schemas import UserCreate, UserResponse, UserUpdate

from .base import BaseAsyncCRUD


class UserCRUD(BaseAsyncCRUD[User, UserCreate, UserUpdate, UserResponse]):

    model = User
    schema = UserCreate
