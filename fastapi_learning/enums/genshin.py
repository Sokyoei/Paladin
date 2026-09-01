import enum


class GenshinRoleQuality(enum.IntEnum):
    four = 4
    five = 5


class GenshinElement(enum.StrEnum):
    # fmt: off
    Anemo = "Anemo"         # 风
    Geo = "Geo"             # 岩
    Electro = "Electro"     # 雷
    Dendro = "Dendro"       # 草
    Hydro = "Hydro"         # 水
    Pyro = "Pyro"           # 火
    Cryo = "Cryo"           # 冰
    # fmt: on
