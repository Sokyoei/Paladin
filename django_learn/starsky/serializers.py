from typing import ClassVar

from rest_framework import serializers

from .models import BlackHole, Constellation, Galaxy, Nebula, Star


class CelestialSerializer(serializers.ModelSerializer):
    class Meta:
        fields: ClassVar[str] = [
            'id',
            'name_zh_cn',
            'name_en_us',
            'discover_year',
            'discoverer',
            'right_ascension',
            'declination',
            'distance_value',
            'distance_unit',
            'description',
            'notes',
            'created_at',
            'updated_at',
        ]


# 各天体专用序列化器
class StarSerializer(CelestialSerializer):
    class Meta(CelestialSerializer.Meta):
        model = Star
        fields: ClassVar[str] = [
            *CelestialSerializer.Meta.fields,
            'mass_value',
            'mass_unit',
            'radius',
            'surface_temperature',
            'spectral_type',
            'luminosity',
            'age',
            'evolution_stage',
        ]


class GalaxySerializer(CelestialSerializer):
    class Meta(CelestialSerializer.Meta):
        model = Galaxy
        fields: ClassVar[str] = [
            *CelestialSerializer.Meta.fields,
            'galaxy_type',
            'hubble_type',
            'diameter',
            'star_count',
            'total_mass_value',
            'total_mass_unit',
            'has_active_nucleus',
        ]


class ConstellationSerializer(CelestialSerializer):
    class Meta(CelestialSerializer.Meta):
        model = Constellation
        fields: ClassVar[str] = [
            *CelestialSerializer.Meta.fields,
            'latin_name',
            'sky_region',
            'bright_star_count',
            'boundary_coords',
            'myth_background',
        ]


class BlackHoleSerializer(CelestialSerializer):
    class Meta(CelestialSerializer.Meta):
        model = BlackHole
        fields: ClassVar[str] = [
            *CelestialSerializer.Meta.fields,
            'black_hole_type',
            'mass_value',
            'mass_unit',
            'event_horizon_radius',
            'spin',
            'host_galaxy',
        ]


class NebulaSerializer(CelestialSerializer):
    class Meta(CelestialSerializer.Meta):
        model = Nebula
        fields: ClassVar[str] = [
            *CelestialSerializer.Meta.fields,
            'nebula_type',
            'size',
            'composition',
            'host_constellation',
        ]
