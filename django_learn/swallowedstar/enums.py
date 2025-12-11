from django.db import models


class SSRealm(models.TextChoices):
    """境界"""

    学徒级 = "学徒级"
    行星级 = "行星级"
    恒星级 = "恒星级"
    宇宙级 = "宇宙级"
    域主级 = "域主级"
    界主级 = "界主级"
    不朽级 = "不朽级"
    尊者级 = "尊者级"


class SSElement(models.TextChoices):
    金 = "金"
    木 = "木"
    水 = "水"
    火 = "火"
    土 = "土"
    雷 = "雷"
    风 = "风"
    空间 = "空间"
    时间 = "时间"


class SSWeaponLevel(models.IntegerChoices):
    学徒级 = 1
    行星级 = 2
    恒星级 = 3
    宇宙级 = 4
    域主级 = 5
    界主级 = 6
    不朽级 = 7
    尊者级 = 8
