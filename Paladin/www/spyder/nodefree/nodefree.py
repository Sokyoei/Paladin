"""
get v2ray nodes
"""

import datetime
from typing import List

import requests
from requests.exceptions import ReadTimeout

from Paladin.www import USER_AGENT


def _get_url(days: int = 1) -> List[List[str]]:
    """get today nodefree.org urls.

    Args:
        days (int): get nearset `n` days.

    Returns:
        list[list[str]]: [url, filename].
    """
    today = datetime.date.today()
    urls = []
    for day in range(days):
        date = today - datetime.timedelta(days=day)
        yyyy = f"{date.year:0>4}"
        m, mm = f"{date.month}", f"{date.month:0>2}"
        dd = f"{date.day:0>2}"
        yyyymmdd = f"{yyyy}{mm}{dd}"

        # https://nodefree.org
        # nodefree = f"https://nodefree.org/dy/{date.year:0>4}/{date.month:0>2}/{yyyymmdd}.txt"
        # urls.append([nodefree, f"nodefree_{yyyymmdd}.txt"])
        # https://nodeclash.github.io/free-nodes/
        for i in range(5):
            nodeclash = f"https://nodeclash.github.io/uploads/{date.year:0>4}/{date.month:0>2}/{i}-{yyyymmdd}.txt"
            urls.append([nodeclash, f"nodeclash_{i}_{yyyymmdd}.txt"])
        # https://tglaoshiji.github.io/clashnodev2raynode/
        tglaoshiji = f"https://tglaoshiji.github.io/nodeshare/{date.year:0>4}/{date.month}/{yyyymmdd}.txt"
        urls.append([tglaoshiji, f"tglaoshiji_{yyyymmdd}.txt"])

    return urls


def download_files(days) -> None:
    """download nodefree.org `v2ray` and `Clash` file.

    Args:
        days (int): see get_url().
    """
    for url, filename in _get_url(days):
        try:
            print(f"start downloading {url} ...")
            req = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
            with open(filename, "w", encoding="utf8") as f:
                f.write(req.text)
            req.close()
            print("success")
        except ReadTimeout:
            print("fail")


"""
vless://2cd6ed0f-636e-4e6c-9449-5a263d7a0fa5@31.22.116.155:443?encryption=none&security=tls&sni=cfed.tgzdyz2.top&type=ws&host=cfed.tgzdyz2.top&path=tg%40zdyz2#GB_%E5%88%86%E4%BA%AB%E6%97%A5%E8%AE%B0
"""


if __name__ == '__main__':
    download_files(days=3)
    print("done.")
