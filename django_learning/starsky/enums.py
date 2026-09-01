from django.db import models


class SpectralTypeChoices(models.TextChoices):
    """恒星光谱类型枚举"""

    O = 'O', 'O'  # noqa: E741
    B = 'B', 'B'
    A = 'A', 'A'
    F = 'F', 'F'
    G = 'G', 'G'
    K = 'K', 'K'
    M = 'M', 'M'
    L = 'L', 'L'
    T = 'T', 'T'
    Y = 'Y', 'Y'


class EvolutionStageChoices(models.TextChoices):
    """恒星演化阶段枚举"""

    MAIN_SEQUENCE = 'MAIN_SEQUENCE', '主序星'
    RED_GIANT = 'RED_GIANT', '红巨星'
    SUPERGIANT = 'SUPERGIANT', '超巨星'
    WHITE_DWARF = 'WHITE_DWARF', '白矮星'
    NEUTRON_STAR = 'NEUTRON_STAR', '中子星'
    BLACK_HOLE = 'BLACK_HOLE', '黑洞前体'
    PROTOSTAR = 'PROTOSTAR', '原恒星'


class GalaxyTypeChoices(models.TextChoices):
    """星系类型枚举"""

    SPIRAL = 'SPIRAL', '旋涡星系'
    ELLIPTICAL = 'ELLIPTICAL', '椭圆星系'
    IRREGULAR = 'IRREGULAR', '不规则星系'
    LENTICULAR = 'LENTICULAR', '透镜星系'


class SkyRegionChoices(models.TextChoices):
    """星座所属天区枚举"""

    NORTHERN_SKY = 'NORTHERN_SKY', '北天星座'
    SOUTHERN_SKY = 'SOUTHERN_SKY', '南天星座'
    ECLIPTIC = 'ECLIPTIC', '黄道星座'


class BlackHoleTypeChoices(models.TextChoices):
    """黑洞类型枚举"""

    STELLAR_MASS = 'STELLAR_MASS', '恒星级黑洞'
    SUPERMASSIVE = 'SUPERMASSIVE', '超大质量黑洞'
    INTERMEDIATE_MASS = 'INTERMEDIATE_MASS', '中等质量黑洞'
    PRIMORDIAL = 'PRIMORDIAL', '原初黑洞'


class NebulaTypeChoices(models.TextChoices):
    """星云类型枚举"""

    EMISSION = 'EMISSION', '发射星云'
    REFLECTION = 'REFLECTION', '反射星云'
    DARK = 'DARK', '暗星云'
    PLANETARY = 'PLANETARY', '行星状星云'
    SUPERNOVA_REMNANT = 'SUPERNOVA_REMNANT', '超新星遗迹'


class DistanceUnitChoices(models.TextChoices):
    """距离单位枚举"""

    LIGHT_YEAR = 'LY', '光年'
    PARSEC = 'PC', '秒差距'
    AU = 'AU', '天文单位'


class MassUnitChoices(models.TextChoices):
    """质量单位枚举（以太阳质量为基准）"""

    SOLAR_MASS = 'M☉', '太阳质量'
    EARTH_MASS = 'M⊕', '地球质量'
