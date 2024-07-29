"""
download GFS/GDAS prepBUFR datasets

"""

from typing import Literal

import requests
from tqdm import tqdm


def _download(urls: list[str]):
    """下载数据"""
    for url in urls:
        req = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (raKHTML, like Gecko)"
                    " Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78 "
                )
            },
            timeout=5,
            stream=True,
        )
        file_name = url.split("/")[-1]
        total = int(req.headers.get("Content-Length", 0))
        with open(file_name, "wb") as f, tqdm(
            desc=file_name, total=total, unit="iB", unit_scale=True, unit_divisor=1024
        ) as t:
            for data in req.iter_content(chunk_size=1024):
                size = f.write(data)
                t.update(size)
        req.close()


def download_gfs(
    date: str,
    sim_hour: Literal["00", "06", "12", "18"],
    start_hour: int,
    end_hour: int,
    degree: Literal["0p25", "0p50", "1p00"],
):
    """下载 gfs 轮换数据"""
    urls = []
    hours = range(start_hour, end_hour + 1, 3)
    for hour in hours:
        url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{sim_hour}/atmos/gfs.t{sim_hour}z.pgrb2.{degree}.f{hour:0>3}"
        urls.append(url)
    _download(urls)


def download_gdas(date: str):
    """下载 gdas prepbufr 轮换数据"""
    urls = []
    for i in range(0, 24, 6):
        url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/obsproc/prod/gdas.{date}/gdas.t{i:0>2}z.prepbufr.nr"
        urls.append(url)
    _download(urls)


def download_ds337_0(date: str):
    """下载历史 prepbufr 数据"""
    urls = []
    url = f"https://data.rda.ucar.edu/ds337.0/tarfiles/{date[:4]}/prepbufr.{date}.nr.tar.gz"
    urls.append(url)
    _download(urls)


def main():
    # download_gfs("20240724", "00", 0, 96, "1p00")
    download_gdas("20240724")
    # download_ds337_0("20240719")
    print("done.")


if __name__ == "__main__":
    main()
