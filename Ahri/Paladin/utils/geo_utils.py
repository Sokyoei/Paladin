"""
geography utils

https://blog.csdn.net/qq_33356563/article/details/83795419
"""

import math


def WGS84_to_WebMercator(lon, lat):
    x = lon * 20037508.342789 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34789 / 180
    return x, y


def WebMercator_to_WGS84(x, y):
    lon = x / 20037508.34 * 180
    lat = y / 20037508.34 * 180
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return lon, lat
