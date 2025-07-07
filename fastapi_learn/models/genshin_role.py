import enum

from sqlalchemy import Column, Date, Enum, String

from .base import Base


class GenshinRoleLevel(enum.IntEnum):
    four = 4
    five = 5


class GenshinRole(Base):
    __tablename__ = "genshin_roles"
    name = Column(String(255), primary_key=True)
    level = Column(Enum(GenshinRoleLevel))
    birthday = Column(Date())
