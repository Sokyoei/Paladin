from typing import ClassVar

from flask_learning.models import Music
from flask_learning.schemas import MusicCreate, MusicResponse, MusicUpdate

from .base import BaseSyncCRUD


class MusicCRUD(BaseSyncCRUD[Music, MusicCreate, MusicUpdate, MusicResponse]):
    model: ClassVar[type[Music]] = Music
    schema: ClassVar[type[MusicResponse]] = MusicResponse
