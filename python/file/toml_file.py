import sys

if sys.version_info >= (3, 11):
    import tomllib  # only read

import tomli_w

with open("../../data/Ahri/Ahri.toml", "rb") as Ahri:
    data = tomllib.load(Ahri)
    print(data)

with open("tempCodeRunnerFile.toml", "wb") as temp:
    tomli_w.dump(data, temp)
