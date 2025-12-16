import uuid
from datetime import datetime

import sqlalchemy
from packaging import version
from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


if version.parse(sqlalchemy.__version__) >= version.parse("1.4"):

    class CreateUpdateAtMixin(Base):
        __abstract__ = True
        created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
        updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    class UUIDMixin(Base):
        __abstract__ = True
        id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    class CreateUpdateByMixin(Base):
        __abstract__ = True
        created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
        updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)

else:
    from sqlalchemy import Column

    class CreateUpdateAtMixin(Base):
        __abstract__ = True
        created_at = Column(DateTime, default=datetime.now)
        updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    class UUIDMixin(Base):
        __abstract__ = True
        id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    class CreateUpdateByMixin(Base):
        __abstract__ = True
        created_by = Column(UUID(as_uuid=True), nullable=True)
        updated_by = Column(UUID(as_uuid=True), nullable=True)
