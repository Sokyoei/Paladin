import uuid

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning.config import settings
from fastapi_learning.models import User
from fastapi_learning.schemas import UserCreate, UserResponse, UserUpdate
from fastapi_learning.utils.password import password_hash

from .base import BaseAsyncCRUD


class UserCRUD(BaseAsyncCRUD[User, UserCreate, UserUpdate, UserResponse]):

    model = User
    schema = UserResponse

    @classmethod
    async def get_by_phone(cls, db: AsyncSession, phone: str) -> User | None:
        result = await db.execute(select(cls.model).where(cls.model.phone == phone))
        return result.unique().scalar_one_or_none()

    @classmethod
    async def get_by_uid(cls, db: AsyncSession, uid: int) -> User | None:
        result = await db.execute(select(cls.model).where(cls.model.uid == uid))
        return result.unique().scalar_one_or_none()

    @classmethod
    async def create(cls, db: AsyncSession, data: UserCreate) -> UserResponse:
        new_uid = await cls.generate_uid(db)
        db_obj = cls.model(
            uid=new_uid,
            hashed_password=password_hash(data.password),
            **data.model_dump(exclude_none=True, exclude_unset=True, exclude={"password"}),
        )
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    async def update(cls, db: AsyncSession, obj_id: uuid.UUID | int | bytes, data: UserUpdate) -> UserResponse | None:
        db_obj = await cls.get(db, obj_id)
        if db_obj:
            for key, value in data.model_dump(exclude_none=True).items():
                if key == "password":
                    value = password_hash(value)
                setattr(db_obj, key, value)
            await db.flush()
            await db.refresh(db_obj)
            return cls.schema.model_validate(db_obj, from_attributes=True)
        return None

    @classmethod
    async def generate_uid(cls, db: AsyncSession) -> int:
        result = await db.execute(select(User.uid).order_by(User.uid.desc()).limit(1))
        max_uid = result.scalar_one_or_none()
        max_uid = max_uid if max_uid else 0

        new_uid = max_uid + 1 if max_uid >= settings.FIRST_UID else settings.FIRST_UID

        async def is_uid_exists(uid: int) -> bool:
            exists_result = await db.execute(select(exists().where(User.uid == uid)))
            return exists_result.scalar_one()

        while await is_uid_exists(new_uid):
            new_uid += 1

        return new_uid
