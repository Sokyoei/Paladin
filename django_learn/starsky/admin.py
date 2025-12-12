from django.contrib import admin

from .models import BlackHole, Constellation, Galaxy, Nebula, Star


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('name_zh_cn', 'name_en_us', 'spectral_type', 'distance_value', 'distance_unit')
    search_fields = ('name_zh_cn', 'name_en_us')


@admin.register(Galaxy)
class GalaxyAdmin(admin.ModelAdmin):
    list_display = ('name_zh_cn', 'name_en_us', 'galaxy_type', 'diameter')
    search_fields = ('name_zh_cn', 'name_en_us')


@admin.register(Constellation)
class ConstellationAdmin(admin.ModelAdmin):
    list_display = ('name_zh_cn', 'name_en_us', 'sky_region')
    search_fields = ('name_zh_cn', 'name_en_us')


@admin.register(BlackHole)
class BlackHoleAdmin(admin.ModelAdmin):
    list_display = ('name_zh_cn', 'name_en_us', 'black_hole_type', 'mass_value', 'host_galaxy')
    search_fields = ('name_zh_cn', 'name_en_us', 'black_hole_type')


@admin.register(Nebula)
class NebulaAdmin(admin.ModelAdmin):
    list_display = ('name_zh_cn', 'name_en_us', 'nebula_type', 'size', 'host_constellation')
    search_fields = ('name_zh_cn', 'name_en_us', 'nebula_type')
