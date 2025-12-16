from abc import ABC
from typing import ClassVar, Generic, Type, TypeVar

from flask_sqlalchemy.model import Model
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)


class BaseAsyncCRUD(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    model: ClassVar[Type[ModelType]]
    schema: ClassVar[Type[ResponseSchemaType]]


class BaseSyncCRUD(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    model: ClassVar[Type[ModelType]]
    schema: ClassVar[Type[ResponseSchemaType]]
