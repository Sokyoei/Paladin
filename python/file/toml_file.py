import sys

if sys.version_info >= (3, 11):
    import tomllib  # only read

import tomli_w

from Paladin import SOKYOEI_DATA_DIR

with open(SOKYOEI_DATA_DIR / "Ahri/Ahri.toml", "rb") as Ahri:
    data = tomllib.load(Ahri)
    print(data)

with open("tempCodeRunnerFile.toml", "wb") as temp:
    tomli_w.dump(data, temp)
