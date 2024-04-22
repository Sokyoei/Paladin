from sqlalchemy import Boolean, Column, Float, String

from . import Base


class Item(Base):
    __tablename__ = "items"
    name = Column(String(255))
    price = Column(Float(255))
    is_offer = Column(Boolean(255))
