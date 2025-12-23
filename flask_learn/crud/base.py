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
    def create(self, obj: CreateSchemaType) -> ResponseSchemaType:
        db_obj = self.model(**obj.model_dump())
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return self.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    def delete(self, obj_id: UUID | int) -> bool:
        db_obj = db.session.get(self.model, obj_id)
        if db_obj:
            db.session.delete(db_obj)
            db.session.commit()
            return True
        return False

    @classmethod
    def update(self, obj_id: UUID | int, obj: UpdateSchemaType) -> ResponseSchemaType | None:
        db_obj = db.session.get(self.model, obj_id)
        if not db_obj:
            return None

        update_data = obj.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.session.commit()
        db.session.refresh(db_obj)
        return self.schema.model_validate(db_obj, from_attributes=True)

    @classmethod
    def search(self, obj_id: UUID | int) -> ResponseSchemaType | None:
        db_obj = db.session.get(self.model, obj_id)
        if db_obj is None:
            return None
        return self.schema.model_validate(db_obj, from_attributes=True)

    get = search

    @classmethod
    def get_all(self) -> list[ResponseSchemaType]:
        db_objs = db.session.query(self.model).all()
        return [self.schema.model_validate(obj, from_attributes=True) for obj in db_objs]
