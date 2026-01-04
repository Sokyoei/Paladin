import uuid
from typing import ClassVar, Type

from werkzeug.security import generate_password_hash

from flask_learn.config import db_instance
from flask_learn.models import User
from flask_learn.schemas import UserCreate, UserResponse, UserUpdate

from .base import BaseSyncCRUD

db = db_instance.db


class UserCRUD(BaseSyncCRUD[User, UserCreate, UserUpdate, UserResponse]):
    model: ClassVar[Type[User]] = User
    schema: ClassVar[Type[UserResponse]] = UserResponse

    @classmethod
    def create(cls, obj: UserCreate):
        db_obj = cls.model(hashed_password=generate_password_hash(obj.password), **obj.model_dump(exclude={"password"}))
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    def update(cls, obj_id: uuid.UUID, obj: UserUpdate):
        db_obj = db.session.get(cls.model, obj_id)
        if not db_obj:
            return None

        update_data = obj.model_dump(exclude_unset=True)
        # 对于密码进行哈希处理
        if "password" in update_data:
            update_data["hashed_password"] = generate_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.session.commit()
        db.session.refresh(db_obj)
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    def get_user_by_email(cls, email: str, orm=False):
        db_obj = cls.model.query.filter_by(email=email).first()
        if not db_obj:
            return None
        return db_obj if orm else cls.schema.model_validate(db_obj, from_attributes=True)
