"""
Generic SQLAlchemy+pydantic CRUD operations.
"""

from abc import ABC
from collections.abc import Callable, Sequence
from typing import cast
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy import ColumnElement, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Load, Session


class Page[ItemType: BaseModel](BaseModel):
    items: list[ItemType] = Field(..., description="当前页数据列表")
    total: int = Field(..., description="满足条件的总记录数")
    page: int = Field(..., description="当前页码")
    per_page: int = Field(..., description="每页记录数")
    total_pages: int = Field(..., description="总页数")


class BaseAsyncCRUD[
    ModelType: DeclarativeBase, CreateSchemaType: BaseModel, UpdateSchemaType: BaseModel, ResponseSchemaType: BaseModel
](ABC):
    """Abstract base class for CRUD operations(async) on a SQLAlchemy model."""

    model: type[ModelType]
    schema: type[ResponseSchemaType]

    @classmethod
    async def create(cls, db: AsyncSession, data: CreateSchemaType) -> ResponseSchemaType:
        factory = cast(Callable[..., ModelType], cls.model)
        db_obj = factory(**data.model_dump(exclude_none=True, exclude_unset=True))
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    async def delete(cls, db: AsyncSession, obj_id: UUID | int | bytes) -> ResponseSchemaType | None:
        db_obj = await db.get(cls.model, obj_id)
        if db_obj:
            await db.delete(db_obj)
            await db.flush()
            return cls.schema.model_validate(db_obj, from_attributes=True)
        return None

    @classmethod
    async def update(
        cls, db: AsyncSession, obj_id: UUID | int | bytes, data: UpdateSchemaType
    ) -> ResponseSchemaType | None:
        db_obj = await db.get(cls.model, obj_id)
        if db_obj:
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            await db.flush()
            await db.refresh(db_obj)
            return cls.schema.model_validate(db_obj, from_attributes=True)
        return None

    @classmethod
    async def search(
        cls, db: AsyncSession, obj_id: UUID | int | bytes, load_options: Sequence[Load] | None = None
    ) -> ResponseSchemaType | None:
        db_obj = await db.get(cls.model, obj_id, options=load_options)
        return cls.schema.model_validate(db_obj, from_attributes=True) if db_obj else None

    get = search

    @classmethod
    async def get_all(
        cls,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 1000,
        load_options: Sequence[Load] | None = None,
        order_by: Sequence[ColumnElement] | None = None,
        **filters: object,
    ) -> list[ResponseSchemaType]:
        conditions = [getattr(cls.model, key) == value for key, value in filters.items()]
        query = select(cls.model)
        if conditions:
            query = query.where(*conditions)
        if order_by is not None:
            query = query.order_by(*order_by)
        query = query.offset(skip).limit(limit)
        if load_options:
            query = query.options(*load_options)
        result = await db.execute(query)
        db_objs = result.scalars().all()
        return [cls.schema.model_validate(db_obj, from_attributes=True) for db_obj in db_objs]

    @classmethod
    async def exists(cls, db: AsyncSession, obj_id: UUID | int | bytes) -> bool:
        return await db.get(cls.model, obj_id) is not None

    @classmethod
    async def count(cls, db: AsyncSession, **filters: object) -> int:
        conditions = [getattr(cls.model, key) == value for key, value in filters.items()]
        stmt = select(func.count()).select_from(cls.model)
        if conditions:
            stmt = stmt.where(*conditions)
        return (await db.execute(stmt)).scalar_one()

    @classmethod
    async def paginate(
        cls,
        db: AsyncSession,
        *,
        page: int = 1,
        per_page: int = 20,
        load_options: Sequence[Load] | None = None,
        order_by: Sequence[ColumnElement] | None = None,
        **filters: object,
    ) -> Page[ResponseSchemaType]:
        order_by = order_by if order_by is not None else [cls.model.created_at.desc()]  # type: ignore[reportAttributeAccessIssue]
        total = await cls.count(db, **filters)
        items = await cls.get_all(
            db, skip=(page - 1) * per_page, limit=per_page, load_options=load_options, order_by=order_by, **filters
        )
        return Page[ResponseSchemaType](
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=(total + per_page - 1) // per_page if per_page else 0,
        )


class BaseSyncCRUD[
    ModelType: DeclarativeBase, CreateSchemaType: BaseModel, UpdateSchemaType: BaseModel, ResponseSchemaType: BaseModel
](ABC):
    """Abstract base class for CRUD operations(sync) on a SQLAlchemy model."""

    model: type[ModelType]
    schema: type[ResponseSchemaType]

    @classmethod
    def create(cls, db: Session, data: CreateSchemaType) -> ResponseSchemaType:
        factory = cast(Callable[..., ModelType], cls.model)
        db_obj = factory(**data.model_dump(exclude_none=True, exclude_unset=True))
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    def delete(cls, db: Session, obj_id: UUID | int | bytes) -> ResponseSchemaType | None:
        db_obj = db.get(cls.model, obj_id)
        if db_obj:
            db.delete(db_obj)
            db.flush()
            return cls.schema.model_validate(db_obj, from_attributes=True)
        return None

    @classmethod
    def update(cls, db: Session, obj_id: UUID | int | bytes, data: UpdateSchemaType) -> ResponseSchemaType | None:
        db_obj = db.get(cls.model, obj_id)
        if db_obj:
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            db.flush()
            db.refresh(db_obj)
            return cls.schema.model_validate(db_obj, from_attributes=True)
        return None

    @classmethod
    def search(
        cls, db: Session, obj_id: UUID | int | bytes, options: Sequence[Load] | None = None
    ) -> ResponseSchemaType | None:
        db_obj = db.get(cls.model, obj_id, options=options)
        return cls.schema.model_validate(db_obj, from_attributes=True) if db_obj else None

    get = search

    @classmethod
    def get_all(
        cls,
        db: Session,
        skip: int = 0,
        limit: int = 1000,
        options: Sequence[Load] | None = None,
        order_by: Sequence[ColumnElement] | None = None,
        **filters: object,
    ) -> list[ResponseSchemaType]:
        conditions = [getattr(cls.model, key) == value for key, value in filters.items()]
        query = select(cls.model)
        if conditions:
            query = query.where(*conditions)
        if order_by is not None:
            query = query.order_by(*order_by)
        query = query.offset(skip).limit(limit)
        if options:
            query = query.options(*options)
        result = db.execute(query)
        db_objs = result.scalars().all()
        return [cls.schema.model_validate(db_obj, from_attributes=True) for db_obj in db_objs]

    @classmethod
    def exists(cls, db: Session, obj_id: UUID | int | bytes) -> bool:
        return db.get(cls.model, obj_id) is not None

    @classmethod
    def count(cls, db: Session, **filters: object) -> int:
        conditions = [getattr(cls.model, key) == value for key, value in filters.items()]
        stmt = select(func.count()).select_from(cls.model)
        if conditions:
            stmt = stmt.where(*conditions)
        return db.execute(stmt).scalar_one()

    @classmethod
    def paginate(
        cls,
        db: Session,
        *,
        page: int = 1,
        per_page: int = 20,
        options: Sequence[Load] | None = None,
        order_by: Sequence[ColumnElement] | None = None,
        **filters: object,
    ) -> Page[ResponseSchemaType]:
        order_by = order_by if order_by is not None else [cls.model.created_at.desc()]  # type: ignore[reportAttributeAccessIssue]
        total = cls.count(db, **filters)
        items = cls.get_all(
            db, skip=(page - 1) * per_page, limit=per_page, options=options, order_by=order_by, **filters
        )
        return Page[ResponseSchemaType](
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=(total + per_page - 1) // per_page if per_page else 0,
        )
