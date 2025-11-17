from django.db import models

# Create your models here.


class GenshinRole(models.Model):
    # fmt:off
    id              = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=30)   # 名字
    level           = models.IntegerField()             # 星级（4星/5星）
    release_version = models.CharField(max_length=200)  # 上线版本
    attribute       = models.CharField(max_length=200)  # 属性（风/水/火/冰/雷/岩/草）
    constellation   = models.CharField(max_length=200)  # 命之座
    birthday        = models.DateTimeField()            # 生日
    affiliation     = models.CharField(max_length=200)  # 所属势力
    special_dish    = models.CharField(max_length=200)  # 特色菜
    # fmt:on
