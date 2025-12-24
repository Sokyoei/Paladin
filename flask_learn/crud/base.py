from abc import ABC
from typing import ClassVar, Generic, Type, TypeVar
from uuid import UUID

from flask_sqlalchemy.model import Model
from pydantic import BaseModel

from flask_learn.config import db_instance

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

db = db_instance.db


class BaseSyncCRUD(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    model: ClassVar[Type[ModelType]]
    schema: ClassVar[Type[ResponseSchemaType]]

    @classmethod
    def create(cls, obj: CreateSchemaType) -> ResponseSchemaType:
        db_obj = cls.model(**obj.model_dump())
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    def delete(cls, obj_id: UUID | int) -> bool:
        db_obj = db.session.get(cls.model, obj_id)
        if db_obj:
            db.session.delete(db_obj)
            db.session.commit()
            return True
        return False

    @classmethod
    def update(cls, obj_id: UUID | int, obj: UpdateSchemaType) -> ResponseSchemaType | None:
        db_obj = db.session.get(cls.model, obj_id)
        if not db_obj:
            return None

        update_data = obj.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.session.commit()
        db.session.refresh(db_obj)
        return cls.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    def search(cls, obj_id: UUID | int, orm=False) -> ModelType | ResponseSchemaType | None:
        db_obj = db.session.get(cls.model, obj_id)
        if db_obj is None:
            return None
        return db_obj if orm else cls.schema.model_validate(db_obj, from_attributes=True)

    get = search

    @classmethod
    def get_all(cls, orm=False) -> list[ModelType] | list[ResponseSchemaType]:
        db_objs = db.session.query(cls.model).all()
        if orm:
            return db_objs
        return [cls.schema.model_validate(obj, from_attributes=True) for obj in db_objs]
