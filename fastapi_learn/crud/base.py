from abc import ABC
from typing import ClassVar, Generic, List, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Session

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)


class BaseAsyncCRUD(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    """Abstract base class for CRUD operations(async) on a SQLAlchemy model."""

    model: ClassVar[Type[ModelType]]
    schema: ClassVar[Type[ResponseSchemaType]]

    @classmethod
    async def create(cls, db: AsyncSession, data: CreateSchemaType) -> ResponseSchemaType:
        try:
            db_obj = cls.model(**data.model_dump(exclude_none=True, exclude_unset=True))
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return cls.schema.model_validate(db_obj, from_attributes=True)
        except SQLAlchemyError:
            await db.rollback()
            raise

    @classmethod
    async def delete(cls, db: AsyncSession, obj_id: UUID | int | bytes) -> Optional[ResponseSchemaType]:
        result = await db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            try:
                await db.delete(db_obj)
                await db.commit()
                return cls.schema.model_validate(db_obj, from_attributes=True)
            except SQLAlchemyError:
                await db.rollback()
                raise
        return None

    @classmethod
    async def update(
        cls, db: AsyncSession, obj_id: UUID | int | bytes, data: UpdateSchemaType
    ) -> Optional[ResponseSchemaType]:
        result = await db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            try:
                update_data = data.model_dump(exclude_unset=True, exclude_none=True)
                for field, value in update_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                await db.commit()
                await db.refresh(db_obj)
                return cls.schema.model_validate(db_obj, from_attributes=True)
            except SQLAlchemyError:
                await db.rollback()
                raise
        return None

    @classmethod
    async def search(cls, db: AsyncSession, obj_id: UUID | int | bytes) -> Optional[ResponseSchemaType]:
        result = await db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            return cls.schema.model_validate(db_obj, from_attributes=True)
        return None

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ResponseSchemaType]:
        result = await db.execute(select(cls.model).offset(skip).limit(limit))
        db_objs = result.scalars().all()
        return [cls.schema.model_validate(db_obj, from_attributes=True) for db_obj in db_objs]


class BaseSyncCRUD(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    """Abstract base class for CRUD operations(sync) on a SQLAlchemy model."""

    model: ClassVar[Type[ModelType]]
    schema: ClassVar[Type[ResponseSchemaType]]

    def create(cls, db: Session, data: CreateSchemaType) -> ResponseSchemaType:
        try:
            db_obj = cls.model(**data.model_dump(exclude_none=True, exclude_unset=True))
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return cls.schema.model_validate(db_obj, from_attributes=True)
        except SQLAlchemyError:
            db.rollback()
            raise

    def delete(cls, db: Session, obj_id: UUID | int | bytes) -> Optional[ResponseSchemaType]:
        result = db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            try:
                db.delete(db_obj)
                db.commit()
                return cls.schema.model_validate(db_obj, from_attributes=True)
            except SQLAlchemyError:
                db.rollback()
                raise
        return None

    def update(cls, db: Session, obj_id: UUID | int | bytes, data: UpdateSchemaType) -> Optional[ResponseSchemaType]:
        result = db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            try:
                update_data = data.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                db.commit()
                db.refresh(db_obj)
                return cls.schema.model_validate(db_obj, from_attributes=True)
            except SQLAlchemyError:
                db.rollback()
                raise
        return None

    def search(cls, db: Session, obj_id: UUID | int | bytes) -> Optional[ResponseSchemaType]:
        result = db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            return cls.schema.model_validate(db_obj, from_attributes=True)
        return None

    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List[ResponseSchemaType]:
        result = db.execute(select(cls.model).offset(skip).limit(limit))
        db_objs = result.scalars().all()
        return [cls.schema.model_validate(db_obj, from_attributes=True) for db_obj in db_objs]
