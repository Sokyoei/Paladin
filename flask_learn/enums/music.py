import enum


class MusicType(enum.StrEnum):
    POP = 'POP'
    UNKNOW = 'UNKNOW'


class MusicLoaction(enum.IntEnum):
    LOCAL = 0
    NETWORK = 1


class MusicTag(enum.IntEnum):
    pass
