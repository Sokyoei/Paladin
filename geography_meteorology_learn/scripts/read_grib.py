"""
读取气象 grib 文件并绘制
"""

from __future__ import annotations

import os

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

from Paladin import PALADIN_ROOT

TOLS = [
    'meanSea',
    'hybrid',
    'atmosphere',
    'surface',
    'planetaryBoundaryLayer',
    'isobaricInPa',
    'isobaricInhPa',
    'heightAboveGround',
    'depthBelowLandLayer',
    'heightAboveSea',
    'atmosphereSingleLayer',
    'lowCloudLayer',
    'middleCloudLayer',
    'highCloudLayer',
    'cloudCeiling',
    'heightAboveGroundLayer',
    'tropopause',
    'maxWind',
    'isothermZero',
    'highestTroposphericFreezing',
    'pressureFromGroundLayer',
    'sigmaLayer',
    'sigma',
    'potentialVorticity',
]
AREA = [115, 41, 123, 32]  # 经纬度网格
resolution = 0.125  # grib 分辨率
SCALE = int(1 / resolution)
AREA_INDEX = [AREA[0] * SCALE, (90 - AREA[1]) * SCALE, AREA[2] * SCALE, (90 - AREA[3]) * SCALE]
print(AREA_INDEX)
SK = 2  # 风场跳过数据的间隔


def read_grib(grib_path: os.PathLike | str):
    grib = xr.open_dataset(grib_path, engine="cfgrib", filter_by_keys={'typeOfLevel': "isobaricInhPa"})
    print(grib)

    # process data
    t = grib["t"].sel(isobaricInhPa=1000)
    u = grib["u"].sel(isobaricInhPa=1000)
    v = grib["v"].sel(isobaricInhPa=1000)
    t.data -= 273.15  # convert K to ℃
    # 截取绘制区域的数据
    tt = t.data[AREA_INDEX[1] : AREA_INDEX[3], AREA_INDEX[0] : AREA_INDEX[2]]
    uu = u.data[AREA_INDEX[1] : AREA_INDEX[3], AREA_INDEX[0] : AREA_INDEX[2]]
    vv = v.data[AREA_INDEX[1] : AREA_INDEX[3], AREA_INDEX[0] : AREA_INDEX[2]]
    lon = grib["longitude"].data[AREA_INDEX[0] : AREA_INDEX[2]]
    lat = grib["latitude"].data[AREA_INDEX[1] : AREA_INDEX[3]]

    # plot t u v
    for var in [tt, uu, vv]:
        fig = plt.figure(figsize=(10, 10))
        ax: GeoAxes = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.coastlines(resolution="10m")
        ax.gridlines()
        ax.add_feature(cfeature.LAND.with_scale("10m"))
        ax.xaxis.set_major_formatter(LongitudeFormatter())
        ax.yaxis.set_major_formatter(LatitudeFormatter())
        ax.set_xticks(np.arange(AREA[0], AREA[2], 1), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(AREA[3], AREA[1], 1), crs=ccrs.PlateCarree())
        contour = ax.contour(lon, lat, var, 10, colors="black", transform=ccrs.PlateCarree())
        plt.clabel(contour, fontsize=15)
        ax.contourf(lon, lat, var, 10, transform=ccrs.PlateCarree(), cmap=matplotlib.colormaps["jet"])
    # grib.t.sel(isobaricInhPa=1000).plot(cmap=plt.cm.coolwarm, transform=ccrs.PlateCarree())

    # plot wind
    fig = plt.figure(figsize=(10, 10))
    ax: GeoAxes = fig.add_subplot(projection=ccrs.PlateCarree())
    ax.coastlines(resolution="10m")
    ax.gridlines()
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.add_feature(cfeature.LAND.with_scale("10m"))
    plt.quiver(
        lon[::SK],
        lat[::SK],
        uu[::SK, ::SK],
        vv[::SK, ::SK],
        color="blue",
        transform=ccrs.PlateCarree(),
        cmap=matplotlib.colormaps["jet"],
    )

    plt.show()


def main():
    # read_grib(PALADIN_ROOT / r"geography_meteorology_learn\data\CMAGFS_NUCLEAR_GLB_20240126000000_00000.grib2")
    read_grib(PALADIN_ROOT / r"geography_meteorology_learn/data/gfs.t00z.pgrb2.0p25.f000")


if __name__ == '__main__':
    main()
