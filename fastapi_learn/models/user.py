from sqlalchemy import Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    account = Column(String(255))
    password = Column(String(255))
