"""
Get v2ray and clash nodes
"""

import datetime
from typing import Dict

import requests
from requests.exceptions import ConnectionError, ReadTimeout

from Ahri.Paladin.www import USER_AGENT

V2RAY = False
CLASH = True
SINGBOX = False


def _get_url(days: int = 1) -> Dict[str, str]:  # noqa: C901
    """get num days nodefree urls.

    Args:
        days (int): get nearset `n` days.

    Returns:
        Dict[str, str]: url: filename.
    """
    today = datetime.date.today()
    # urls = []
    urls: Dict[str, str] = {}
    for day in range(days):
        date = today - datetime.timedelta(days=day)
        yyyy = f"{date.year:0>4}"
        m = f"{date.month}"
        mm = f"{date.month:0>2}"
        dd = f"{date.day:0>2}"
        yyyymmdd = f"{yyyy}{mm}{dd}"

        ################################################################################################################
        # fmt: off

        # https://nodefree.org/
        if V2RAY:
            urls[f"https://nodefree.githubrowcontent.com/{yyyy}/{mm}/{yyyymmdd}.txt"] = f"nodefree_org_{yyyymmdd}.txt"
        if CLASH:
            urls[f"https://nodefree.githubrowcontent.com/{yyyy}/{mm}/{yyyymmdd}.yaml"] = f"nodefree_org_{yyyymmdd}.yaml"

        # https://nodeclash.github.io/free-nodes/
        for i in range(5):
            if V2RAY:
                urls[f"https://node.freeclashnode.com/uploads/{yyyy}/{mm}/{i}-{yyyymmdd}.txt"] = f"nodeclash_{i}_{yyyymmdd}.txt"
            if CLASH:
                urls[f"https://node.freeclashnode.com/uploads/{yyyy}/{mm}/{i}-{yyyymmdd}.yaml"] = f"nodeclash_{i}_{yyyymmdd}.yaml"

        # https://tglaoshiji.github.io/clashnodev2raynode/
        if V2RAY:
            urls[f"https://a.nodeshare.xyz/uploads/{yyyy}/{m}/{yyyymmdd}.txt"] = f"tglaoshiji_{yyyymmdd}.txt"
        if CLASH:
            urls[f"https://a.nodeshare.xyz/uploads/{yyyy}/{m}/{yyyymmdd}.yaml"] = f"tglaoshiji_{yyyymmdd}.yaml"

        # https://clashfreenode.com/
        if V2RAY:
            urls[f"https://clashfreenode.com/feed/v2ray-{yyyymmdd}.txt"] = f"clashfreenode_{yyyymmdd}.txt"
        if CLASH:
            urls[f"https://clashfreenode.com/feed/clash-{yyyymmdd}.yaml"] = f"clashfreenode_{yyyymmdd}.yaml"


        # https://nodefree.cc/
        for i in range(5):
            if V2RAY:
                urls[f"https://node.nodefree.cc/uploads/{yyyy}/{mm}/{i}-{yyyymmdd}.txt"] = f"nodefree_cc_{i}_{yyyymmdd}.txt"
            if CLASH:
                urls[f"https://node.nodefree.cc/uploads/{yyyy}/{mm}/{i}-{yyyymmdd}.yaml"] = f"nodefree_cc_{i}_{yyyymmdd}.yaml"

        # fmt: on
        ################################################################################################################

    return urls


def download_files(days: int) -> None:
    """download nodefree `v2ray` and `clash` file.

    Args:
        days (int): see get_url().
    """
    for url, filename in _get_url(days).items():
        try:
            print(f"start downloading {url} ...")
            req = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
            with open(filename, "w", encoding="utf8") as f:
                f.write(req.text)
            req.close()
            print("success")
        except (ReadTimeout, ConnectionError):
            print("fail")


def main():
    download_files(days=3)
    print("done.")


"""
vless://2cd6ed0f-636e-4e6c-9449-5a263d7a0fa5@31.22.116.155:443?encryption=none&security=tls&sni=cfed.tgzdyz2.top&type=ws&host=cfed.tgzdyz2.top&path=tg%40zdyz2#GB_%E5%88%86%E4%BA%AB%E6%97%A5%E8%AE%B0
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIjN8ZCoqKioqKioqKmcuY29tXzIgIzEiLA0KICAiYWRkIjogIjEwNC4xOS41MS4yMzIiLA0KICAicG9ydCI6ICIyMDg2IiwNCiAgImlkIjogIjI5ZWViYjYwLWIyN2ItNGE5ZC1iYmE1LTk0Nzc2M2Q5MjA1ZSIsDQogICJhaWQiOiAiMCIsDQogICJzY3kiOiAiYXV0byIsDQogICJuZXQiOiAid3MiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAiaXAwMDYuMzE5Njc3Mi54eXoiLA0KICAicGF0aCI6ICJnaXRodWIuY29tL0FsdmluOTk5OSIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICJpcDAwNi4zMTk2NzcyLnh5eiIsDQogICJhbHBuIjogIiIsDQogICJmcCI6ICIiDQp9
"""

if __name__ == '__main__':
    main()
