import os
from pathlib import Path

PALADIN_ROOT = Path(__file__).resolve().parent.parent

sokyoei_data_dir = os.environ.get("SOKYOEI_DATA_DIR")
if sokyoei_data_dir:
    SOKYOEI_DATA_DIR = Path(sokyoei_data_dir)
else:
    raise KeyError("SOKYOEI_DATA_DIR are not set, please set this environment variable.")
