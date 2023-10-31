import sys

if sys.version_info >= (3, 11):
    import tomllib

    with open("../../data/Ahri/Ahri.toml", "rb") as Ahri:
        data = tomllib.load(Ahri)
        print(data)
