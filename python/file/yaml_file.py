import yaml

from Ahri.Paladin import SOKYOEI_DATA_DIR

# yaml -> dict
with open(SOKYOEI_DATA_DIR / "Ahri/Ahri.yaml", encoding="utf8") as Ahri:
    data = yaml.load(Ahri, Loader=yaml.FullLoader)
    print(data)

# dict -> yaml
with open("tempCodeRunnerFile.yaml", "w", encoding="utf8") as temp:
    yaml.dump(data, temp, allow_unicode=True)
