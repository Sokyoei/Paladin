from sqlalchemy import exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learn.config.config import FIRST_UID
from fastapi_learn.models import User
from fastapi_learn.schemas import UserCreate, UserResponse, UserUpdate
from fastapi_learn.utils.password import password_hash

from .base import BaseAsyncCRUD


class UserCRUD(BaseAsyncCRUD[User, UserCreate, UserUpdate, UserResponse]):

    model = User
    schema = UserResponse

    @classmethod
    async def create(cls, db: AsyncSession, data: UserCreate) -> UserResponse:
        new_uid = await cls.__generate_uid(db)
        try:
            db_obj = cls.model(
                uid=new_uid,
                password=password_hash(data.password),
                **data.model_dump(exclude_none=True, exclude_unset=True, exclude={"password"}),
            )
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return cls.schema.model_validate(db_obj, from_attributes=True)
        except SQLAlchemyError:
            await db.rollback()
            raise

    @classmethod
    async def __generate_uid(cls, db: AsyncSession) -> int:
        result = await db.execute(select(User.uid).order_by(User.uid.desc()).limit(1))
        max_uid = result.scalar_one_or_none()
        max_uid = max_uid if max_uid else 0

        new_uid = max_uid + 1 if max_uid >= FIRST_UID else FIRST_UID

        async def is_uid_exists(uid: int) -> bool:
            exists_result = await db.execute(select(exists().where(User.uid == uid)))
            return exists_result.scalar_one()

        while await is_uid_exists(new_uid):
            new_uid += 1

        return new_uid

    @classmethod
    async def get_user_by_account(cls, db: AsyncSession, account: str) -> UserResponse | None:
        result = await db.execute(select(User).where(User.account == account))
        user = result.scalar_one_or_none()
        return cls.schema.model_validate(user, from_attributes=True) if user else None

    @classmethod
    async def get_user_by_uid(cls, db: AsyncSession, uid: int) -> UserResponse | None:
        result = await db.execute(select(User).where(User.uid == uid))
        user = result.scalar_one_or_none()
        return cls.schema.model_validate(user, from_attributes=True) if user else None
