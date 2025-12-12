from typing import ClassVar

from django.db import models

from django_learn.utils.django_utils import CreateUpdateAtModel, CreateUpdateByModel, UUIDModel

from .enums import (
    BlackHoleTypeChoices,
    DistanceUnitChoices,
    EvolutionStageChoices,
    GalaxyTypeChoices,
    MassUnitChoices,
    NebulaTypeChoices,
    SkyRegionChoices,
    SpectralTypeChoices,
)


class Celestial(UUIDModel, CreateUpdateAtModel, CreateUpdateByModel):
    """
    天体抽象基类：提取所有天体的通用字段，不生成实际数据表
    """

    # 基础信息
    name_zh_cn = models.CharField(max_length=100, verbose_name='中文名称')
    name_en_us = models.CharField(max_length=100, blank=True, null=True, verbose_name='英文名称/拉丁名')
    discover_year = models.IntegerField(blank=True, null=True, verbose_name='发现年份')
    discoverer = models.CharField(max_length=100, blank=True, null=True, verbose_name='发现者')

    # 空间坐标（天文学标准：赤经/赤纬）
    right_ascension = models.CharField(max_length=50, blank=True, null=True, verbose_name='赤经 (hh:mm:ss)')
    declination = models.CharField(max_length=50, blank=True, null=True, verbose_name='赤纬 (±dd:mm:ss)')

    # 距离信息
    distance_value = models.DecimalField(
        max_digits=20, decimal_places=4, blank=True, null=True, verbose_name='距离数值'
    )
    distance_unit = models.CharField(
        max_length=10, choices=DistanceUnitChoices.choices, blank=True, null=True, verbose_name='距离单位'
    )

    # 描述信息
    description = models.TextField(blank=True, null=True, verbose_name='天体描述')
    notes = models.TextField(blank=True, null=True, verbose_name='补充说明')

    class Meta:
        abstract = True
        verbose_name = '天体（抽象）'
        verbose_name_plural = '天体（抽象）'
        ordering: ClassVar[str] = ['name_zh_cn']  # 默认按中文名称排序

    def __str__(self):
        return f'{self.name_zh_cn} ({self.name_en_us or "无英文名"})'


class Star(Celestial):
    """
    恒星模型：特有属性包括质量、半径、温度、光谱类型等
    """

    mass_value = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True, verbose_name='质量数值')
    mass_unit = models.CharField(
        max_length=10, choices=MassUnitChoices.choices, blank=True, null=True, verbose_name='质量单位'
    )
    radius = models.DecimalField(
        max_digits=20, decimal_places=4, blank=True, null=True, verbose_name='半径 (太阳半径 R☉)'
    )
    surface_temperature = models.IntegerField(blank=True, null=True, verbose_name='表面温度 (K)')
    spectral_type = models.CharField(
        max_length=10, choices=SpectralTypeChoices.choices, blank=True, null=True, verbose_name='光谱类型'
    )
    luminosity = models.DecimalField(
        max_digits=20, decimal_places=4, blank=True, null=True, verbose_name='光度 (太阳光度 L☉)'
    )
    age = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True, verbose_name='年龄 (亿年)')
    evolution_stage = models.CharField(
        max_length=50, choices=EvolutionStageChoices.choices, blank=True, null=True, verbose_name='演化阶段'
    )

    class Meta:
        verbose_name = '恒星'
        verbose_name_plural = '恒星'

    def __str__(self):
        return f'恒星: {self.name_zh_cn} ({self.spectral_type or "未知光谱型"})'


class Galaxy(Celestial):
    """
    星系模型：特有属性包括类型、直径、恒星数量等
    """

    galaxy_type = models.CharField(
        max_length=50, choices=GalaxyTypeChoices.choices, blank=True, null=True, verbose_name='星系类型'
    )
    hubble_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='哈勃分类（如Sa/Sb/Sc）')
    diameter = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True, verbose_name='直径 (光年)')
    star_count = models.CharField(max_length=50, blank=True, null=True, verbose_name='恒星数量（如"约1000亿颗"）')
    total_mass_value = models.DecimalField(
        max_digits=30, decimal_places=4, blank=True, null=True, verbose_name='总质量数值'
    )
    total_mass_unit = models.CharField(
        max_length=10, choices=MassUnitChoices.choices, blank=True, null=True, verbose_name='总质量单位'
    )
    has_active_nucleus = models.BooleanField(default=False, verbose_name='是否有活动星系核')

    class Meta:
        verbose_name = '星系'
        verbose_name_plural = '星系'

    def __str__(self):
        return f'星系: {self.name_zh_cn} ({self.galaxy_type or "未知类型"})'


class Constellation(Celestial):
    """
    星座模型：特有属性包括所属天区、亮星数量、神话背景等
    """

    latin_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='拉丁正式名称')
    sky_region = models.CharField(
        max_length=50, choices=SkyRegionChoices.choices, blank=True, null=True, verbose_name='所属天区'
    )
    bright_star_count = models.IntegerField(blank=True, null=True, verbose_name='亮星数量（视星等<6等）')
    boundary_coords = models.TextField(blank=True, null=True, verbose_name='边界坐标（天球坐标范围）')
    myth_background = models.TextField(blank=True, null=True, verbose_name='神话背景')

    class Meta:
        verbose_name = '星座'
        verbose_name_plural = '星座'

    def __str__(self):
        return f'星座: {self.name_zh_cn} ({self.latin_name or "未知拉丁名"})'


class BlackHole(Celestial):
    """
    黑洞模型：特有属性包括类型、事件视界、自旋、所属星系等
    """

    black_hole_type = models.CharField(
        max_length=50, choices=BlackHoleTypeChoices.choices, blank=True, null=True, verbose_name='黑洞类型'
    )
    mass_value = models.DecimalField(
        max_digits=30, decimal_places=4, blank=True, null=True, verbose_name='黑洞质量数值'
    )
    mass_unit = models.CharField(
        max_length=10, choices=MassUnitChoices.choices, blank=True, null=True, verbose_name='黑洞质量单位'
    )
    event_horizon_radius = models.DecimalField(
        max_digits=20, decimal_places=4, blank=True, null=True, verbose_name='事件视界半径 (km)'
    )
    spin = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, verbose_name='自旋参数 (0-1)')
    # 关联所属星系（外键，星系删除时黑洞设为无所属）
    host_galaxy = models.ForeignKey(
        Galaxy, on_delete=models.SET_NULL, blank=True, null=True, related_name='black_holes', verbose_name='所属星系'
    )

    class Meta:
        verbose_name = '黑洞'
        verbose_name_plural = '黑洞'

    def __str__(self):
        return f'黑洞: {self.name_zh_cn} ({self.black_hole_type or "未知类型"})'


class Nebula(Celestial):
    """
    星云模型：特有属性包括类型、组成成分、所在星座等
    """

    nebula_type = models.CharField(
        max_length=50, choices=NebulaTypeChoices.choices, blank=True, null=True, verbose_name='星云类型'
    )
    size = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True, verbose_name='大小 (光年)')
    composition = models.CharField(max_length=200, blank=True, null=True, verbose_name='主要组成成分（如H₂, He, 尘埃）')
    # 关联所在星座（外键，星座删除时星云设为无所属）
    host_constellation = models.ForeignKey(
        Constellation, on_delete=models.SET_NULL, blank=True, null=True, related_name='nebulae', verbose_name='所在星座'
    )

    class Meta:
        verbose_name = '星云'
        verbose_name_plural = '星云'

    def __str__(self):
        return f'星云: {self.name_zh_cn} ({self.nebula_type or "未知类型"})'
