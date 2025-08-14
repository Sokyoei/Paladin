"""
读取气象 netCDF 数据并绘制
"""

from __future__ import annotations

import os

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from matplotlib import pyplot as plt
from netCDF4 import Dataset
from wrf import getvar

from Ahri.Paladin import PALADIN_ROOT

SK = 3  # 风场跳过数据的间隔


def read_netcdf_wrfout(path: os.PathLike | str):
    nc = Dataset(path)
    print(nc.variables.keys())

    # process data
    t = getvar(nc, "tc", 0, meta=False)
    u = getvar(nc, "ua", 0, meta=False)
    v = getvar(nc, "va", 0, meta=False)
    z = getvar(nc, "z", 0)  # noqa: F841
    p = getvar(nc, "pressure", 0, meta=False)  # noqa: F841
    lon = getvar(nc, "lon", 0, meta=False)
    lat = getvar(nc, "lat", 0, meta=False)
    # 截取 t u v 最下层数据（近似 1000hpa）
    tt = t[0]
    uu = u[0]
    vv = v[0]

    # plot t u v
    for var in [tt, uu, vv]:
        fig = plt.figure(figsize=(10, 10))
        ax: GeoAxes = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.coastlines(resolution="10m")
        ax.gridlines()
        ax.xaxis.set_major_formatter(LongitudeFormatter())
        ax.yaxis.set_major_formatter(LatitudeFormatter())
        ax.add_feature(cfeature.LAND.with_scale("10m"))
        contour = ax.contour(lon, lat, var, 10, colors="black", transform=ccrs.PlateCarree())
        plt.clabel(contour, fontsize=15)
        ax.contourf(lon, lat, var, 10, transform=ccrs.PlateCarree(), cmap=matplotlib.colormaps["jet"])

    # plot wind
    fig = plt.figure(figsize=(10, 10))
    ax: GeoAxes = fig.add_subplot(projection=ccrs.PlateCarree())
    ax.coastlines(resolution="10m")
    ax.gridlines()
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.add_feature(cfeature.LAND.with_scale("10m"))
    ax.gridlines()
    plt.quiver(
        lon[::SK, ::SK],
        lat[::SK, ::SK],
        uu[::SK, ::SK],
        vv[::SK, ::SK],
        color="blue",
        transform=ccrs.PlateCarree(),
        cmap=matplotlib.colormaps["jet"],
    )

    plt.show()


def main():
    read_netcdf_wrfout(PALADIN_ROOT / r"geography_meteorology_learn\data\wrfout_d01_2024-08-05_00_00_00")


if __name__ == '__main__':
    main()
