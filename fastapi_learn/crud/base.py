from abc import ABC
from typing import ClassVar, Generic, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseCRUD(ABC, Generic[ModelType, SchemaType]):
    """Abstract base class for CRUD operations on a SQLAlchemy model."""

    model: ClassVar[Type[ModelType]]
    schema: ClassVar[Type[SchemaType]]

    @classmethod
    async def create(cls, db: AsyncSession, data: SchemaType) -> SchemaType:
        try:
            db_obj = cls.model(**data.model_dump(exclude_unset=True))
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return cls.schema.model_validate(db_obj)
        except SQLAlchemyError:
            await db.rollback()
            raise

    @classmethod
    async def delete(cls, db: AsyncSession, obj_id: UUID) -> Optional[SchemaType]:
        result = await db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            try:
                await db.delete(db_obj)
                await db.commit()
                return cls.schema.model_validate(db_obj)
            except SQLAlchemyError:
                await db.rollback()
                raise
        return None

    @classmethod
    async def update(cls, db: AsyncSession, obj_id: UUID, data: SchemaType) -> Optional[SchemaType]:
        result = await db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            try:
                update_data = data.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                await db.commit()
                await db.refresh(db_obj)
                return cls.schema.model_validate(db_obj)
            except SQLAlchemyError:
                await db.rollback()
                raise
        return None

    @classmethod
    async def search(cls, db: AsyncSession, obj_id: UUID) -> Optional[SchemaType]:
        result = await db.execute(select(cls.model).filter(cls.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            return cls.schema.model_validate(db_obj)
        return None
