from django.db import models

from django_learn.utils.django_utils import CreateUpdateAtModel, CreateUpdateByModel, UUIDModel

from .enums import SSElement, SSRealm


class SwallowedStarRole(UUIDModel, CreateUpdateAtModel, CreateUpdateByModel):
    name = models.CharField(max_length=100, null=False, verbose_name="角色名称")
    title = models.CharField(max_length=255, null=True, verbose_name="角色称号")
    realm = models.CharField(max_length=100, choices=SSRealm, null=False, verbose_name="角色境界")
    element = models.CharField(max_length=100, choices=SSElement, null=True, verbose_name="元素")

    class Meta:
        db_table = "swallowed_star_role"
