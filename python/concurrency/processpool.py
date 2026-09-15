# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     notebook_metadata_filter: -all,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
# ---

# %% [markdown]
# # Python 进程池
#
# <div style="border: 1px solid #ffcc00; padding:1em; border-left:4px solid #f59e0b; margin:1em 0;">
#   <strong>⚠️WARNING</strong>
#     <a href="https://docs.python.org/zh-cn/3/library/multiprocessing.html#using-a-pool-of-workers">
#       <p>交互环境下 <code>mp.Pool</code>, <code>ProcessPoolExecutor</code> 无法运行！</p>
#     </a>
# </div>

# %%
import logging
import multiprocessing as mp
import urllib.request
from concurrent.futures import ProcessPoolExecutor, as_completed
from urllib.error import HTTPError, URLError

from loguru import logger
from pydantic import BaseModel, Field

from paladin.config import settings

# %%
BAIDU_URL: str = "https://www.baidu.com"
GOOGLE_URL: str = "https://www.google.com"
JD_URL: str = "https://www.jd.com"
URLS: list[str] = [
    BAIDU_URL,
    GOOGLE_URL,
    JD_URL,
    "https://www.taobao.com",
    "https://www.sina.com.cn",
    "https://www.163.com",
    "https://www.qq.com",
    "https://www.yahoo.com",
    "https://www.youtube.com",
    "https://www.twitter.com",
    "https://www.facebook.com",
    "https://www.instagram.com",
]


# %%
class DownloadResult(BaseModel):
    url: str = Field(..., description="下载 URL")
    ok: bool = Field(..., description="是否成功")
    status_code: int | None = Field(None, description="状态码")
    content_len: int = Field(0, description="内容长度")
    error: str | None = Field(None, description="错误信息")


# %%
def download_worker(url: str, timeout: float = 3.0) -> DownloadResult:
    ok: bool = False
    status_code: int | None = None
    content_len = 0
    error: str | None = None

    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"

    try:
        logger.info(f"开始请求: {url}")
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            status_code = resp.getcode()
            html = resp.read()
            logger.info(f"成功 {url}, status={status_code}, len={len(html)}")
            ok = True
            content_len = len(html)
    except HTTPError as e:
        logger.warning(f"HTTP 错误 {url}, code={e.code}, msg={e.reason}")
        error = str(e)
    except URLError as e:
        logger.warning(f"URL 错误 {url}, reason={e.reason}")
        error = str(e)
    except TimeoutError as e:
        logger.warning(f"超时: {url}: {e}")
        error = str(e)
    except Exception as e:
        logger.exception(f"未知异常 {url}: {e}")
        error = str(e)

    return DownloadResult(url=url, ok=ok, status_code=status_code, content_len=content_len, error=error)


# %% [markdown]
# ## [ProcessPoolExecutor](https://docs.python.org/zh-cn/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor)


# %%
def concurrent_futures_ProcessPoolExecutor_example():
    with ProcessPoolExecutor(max_workers=4) as pool:
        logger.debug("submit, 提交单个任务")
        pool.submit(download_worker, BAIDU_URL)

        logger.debug("map, 批量提交任务")
        pool.map(download_worker, URLS)

        logger.debug("as_completed, 获取任务结果")
        futures = [pool.submit(download_worker, url) for url in URLS]
        for future in as_completed(futures):
            logger.info(future.result())


# %% [markdown]
# ## [Pool](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.pool.Pool)


# %%
def mp_Pool_example():
    with mp.Pool(processes=4) as pool:
        logger.debug("apply, 同步阻塞，执行单个任务")
        result_apply = pool.apply(download_worker, args=(BAIDU_URL,))
        logger.info(f"{result_apply=}")

        logger.debug("apply_async, 异步非阻塞，执行单个任务")
        result_apply_async = pool.apply_async(download_worker, args=(BAIDU_URL,))
        logger.info(f"{result_apply_async.ready()=}")
        logger.info(f"{result_apply_async.get()=}")

        logger.debug("map, 同步阻塞，批量执行任务，单参数，func()/func(x)")
        result_map = pool.map(download_worker, URLS)
        logger.info(f"{result_map=}")

        logger.debug("map_async, 异步非阻塞，批量执行任务")
        result_map_async = pool.map_async(download_worker, URLS)
        logger.info(f"{result_map_async.ready()=}")
        logger.info(f"{result_map_async.get()=}")

        logger.debug("starmap, 同步阻塞，批量执行任务，参数为元组，func(*args)")
        result_starmap = pool.starmap(download_worker, [(BAIDU_URL, 2.0), (GOOGLE_URL, 2.0), (JD_URL, 2.0)])
        logger.info(f"{result_starmap=}")

        logger.debug("starmap_async, 异步非阻塞，批量执行任务，参数为元组")
        result_starmap_async = pool.starmap_async(download_worker, [(BAIDU_URL, 2.0), (GOOGLE_URL, 2.0), (JD_URL, 2.0)])
        logger.info(f"{result_starmap_async.ready()=}")
        logger.info(f"{result_starmap_async.get()=}")

        logger.debug("imap, 迭代执行任务，有序，内存友好")
        result_imap = pool.imap(download_worker, URLS)
        for result in result_imap:
            logger.info(f"{result=}")

        logger.debug("imap_unordered, 同步迭代执行任务，无序，内存友好")
        result_imap_unordered = pool.imap_unordered(download_worker, URLS)
        for result in result_imap_unordered:
            logger.info(f"{result=}")


# %%
def main():
    concurrent_futures_ProcessPoolExecutor_example()
    mp_Pool_example()


# %%
if __name__ == "__main__":
    if settings.DEBUG:
        mp_logger = mp.log_to_stderr(logging.DEBUG)
        mp_logger.info("multiprocessing debug log enabled.")

    main()
