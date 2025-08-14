"""
download GFS/GDAS prepBUFR datasets
"""

from typing import Literal

from Ahri.Paladin.utils import download_file


def download_gfs(
    date: str,
    sim_hour: Literal["00", "06", "12", "18"],
    start_hour: int,
    end_hour: int,
    degree: Literal["0p25", "0p50", "1p00"],
):
    """下载 gfs 轮换数据"""
    hours = range(start_hour, end_hour + 1, 3)
    for hour in hours:
        url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{sim_hour}/atmos/gfs.t{sim_hour}z.pgrb2.{degree}.f{hour:0>3}"
        download_file(url)


def download_gdas(date: str):
    """下载 gdas prepbufr 轮换数据"""
    for i in range(0, 24, 6):
        url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/obsproc/prod/gdas.{date}/gdas.t{i:0>2}z.prepbufr.nr"
        download_file(url)


def download_ds337_0(date: str):
    """下载历史 prepbufr 数据"""
    url = f"https://data.rda.ucar.edu/ds337.0/tarfiles/{date[:4]}/prepbufr.{date}.nr.tar.gz"
    download_file(url)


def main():
    # download_gfs("20240724", "00", 0, 96, "1p00")
    # download_gdas("20240724")
    # download_ds337_0("20240719")
    print("done.")


if __name__ == "__main__":
    main()
