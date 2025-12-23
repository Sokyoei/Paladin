from typing import ClassVar, Type

from flask_learn.models import Music
from flask_learn.schemas import MusicCreate, MusicResponse, MusicUpdate

from .base import BaseSyncCRUD


class MusicCRUD(BaseSyncCRUD[Music, MusicCreate, MusicUpdate, MusicResponse]):
    model: ClassVar[Type[Music]] = Music
    schema: ClassVar[Type[MusicResponse]] = MusicResponse
