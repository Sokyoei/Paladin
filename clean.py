import shutil
from pathlib import Path

ROOT = Path(".").resolve().parent
site = ROOT / "site"  # mkdocs build dir


def recurse_remove(pattern: str, path: Path = ROOT, del_file=True, del_dir=False):
    """递归删除文件或文件夹

    Args:
        pattern (str): 匹配的文件名
        path (Path, optional): 路径. Defaults to ROOT.
        del_file (bool, optional): 是否删除文件. Defaults to True.
        del_dir (bool, optional): 是否删除文件夹. Defaults to False.
    """
    for f in path.rglob(pattern):
        if del_file and f.is_file():
            f.unlink()
        if del_dir and f.is_dir():
            shutil.rmtree(f)


def main():
    if site.exists():
        shutil.rmtree(site)
    recurse_remove("__pycache__")
    recurse_remove(".pytest_cache")
    recurse_remove(".ipynb_checkpoints")
    recurse_remove("build")
    recurse_remove("target")
    recurse_remove("*.pyd")
    recurse_remove("*.dll")
    recurse_remove("*.mod")
    recurse_remove("*.lock")
    recurse_remove("*.lib")
    recurse_remove("*.a")
    recurse_remove("*.obj")
    recurse_remove("tempCodeRunnerFile.*")


if __name__ == "__main__":
    main()
