"""
Get v2ray and clash nodes
"""

import datetime
from typing import List

import requests
from requests.exceptions import ConnectionError, ReadTimeout

from Paladin.www import USER_AGENT


def _get_url(days: int = 1) -> List[List[str]]:
    """get num days nodefree urls.

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
        m = f"{date.month}"
        mm = f"{date.month:0>2}"
        dd = f"{date.day:0>2}"
        yyyymmdd = f"{yyyy}{mm}{dd}"

        ################################################################################################################
        # https://nodefree.org
        # nodefree = f"https://nodefree.org/dy/{yyyy}/{mm}/{yyyymmdd}.txt"
        # urls.append([nodefree, f"nodefree_{yyyymmdd}.txt"])
        nodefree_v2ray = f"https://nodefree.githubrowcontent.com/{yyyy}/{mm}/{yyyymmdd}.txt"
        urls.append([nodefree_v2ray, f"nodefree_{yyyymmdd}.txt"])
        nodefree_clash = f"https://nodefree.githubrowcontent.com/{yyyy}/{mm}/{yyyymmdd}.yaml"
        urls.append([nodefree_clash, f"nodefree_{yyyymmdd}.yaml"])

        # https://nodeclash.github.io/free-nodes/
        for i in range(5):
            # nodeclash = f"https://nodeclash.github.io/uploads/{date.year:0>4}/{date.month:0>2}/{i}-{yyyymmdd}.txt"
            nodeclash = f"https://www.freeclashnode.com/uploads/{yyyy}/{mm}/{i}-{yyyymmdd}.txt"
            urls.append([nodeclash, f"nodeclash_{i}_{yyyymmdd}.txt"])

        # https://tglaoshiji.github.io/clashnodev2raynode/
        # tglaoshiji = f"https://tglaoshiji.github.io/nodeshare/{yyyy}/{m}/{yyyymmdd}.txt"
        # urls.append([tglaoshiji, f"tglaoshiji_{yyyymmdd}.txt"])
        tglaoshiji_clash = f"https://a.nodeshare.xyz/uploads/{yyyy}/{m}/{yyyymmdd}.yaml"
        urls.append([tglaoshiji_clash, f"tglaoshiji_{yyyymmdd}.yaml"])

        # https://clashfreenode.com/
        clashfreenode_v2ray = f"https://clashfreenode.com/feed/v2ray-{yyyymmdd}.txt"
        urls.append([clashfreenode_v2ray, f"v2ray-{yyyymmdd}.txt"])
        clashfreenode_clash = f"https://clashfreenode.com/feed/clash-{yyyymmdd}.yaml"
        urls.append([clashfreenode_clash, f"v2ray-{yyyymmdd}.yaml"])
        ################################################################################################################

    return urls


def download_files(days: int) -> None:
    """download nodefree `v2ray` and `clash` file.

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
