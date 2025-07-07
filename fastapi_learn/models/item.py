from sqlalchemy import Boolean, Column, Float, String

from .base import Base


class Item(Base):
    __tablename__ = "items"
    name = Column(String(255), primary_key=True)
    price = Column(Float(255))
    is_offer = Column(Boolean(255))
