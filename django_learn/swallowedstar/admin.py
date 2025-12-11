from typing import ClassVar

from django.contrib import admin

from .models import SwallowedStarRole


@admin.register(SwallowedStarRole)
class SwallowedStarRoleAdmin(admin.ModelAdmin):
    list_display: ClassVar[list[str]] = ['id', 'name', 'title', 'realm', 'element']
    list_filter: ClassVar[list[str]] = ['realm', 'element']
    search_fields: ClassVar[list[str]] = ['name', 'title']
    ordering: ClassVar[list[str]] = ['name']
