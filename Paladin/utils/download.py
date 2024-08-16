from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm

from Paladin.www import USER_AGENT


def download_file(url: str, dst_path: Optional[str | os.PathLike] = None, check_exists: bool = True):
    """下载文件

    Args:
        url (str): 文件在网络上的地址。
        dst_path (Optional[str | os.PathLike]): 保存路径。默认是 None, 为当前路径。
        check_exists (bool): 是否检查文件存在。默认是 True.
    """
    file_name = url.split("/")[-1] if dst_path is None else dst_path
    if (check_exists and not Path(file_name).exists()) or not check_exists:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        total = int(response.headers.get("Content-Length", 0))
        with open(file_name, "wb") as f, tqdm(
            desc=file_name, total=total, unit="iB", unit_scale=True, unit_divisor=1024
        ) as t:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                t.update(size)
        response.close()
