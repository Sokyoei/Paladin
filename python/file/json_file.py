import json

from Paladin import SOKYOEI_DATA_DIR

# json -> dict
with open(SOKYOEI_DATA_DIR / "Ahri/Ahri.json", "r", encoding="utf8") as Ahri:
    data = json.load(Ahri)
    print(data)

# dict -> json
with open("tempCodeRunnerFile.json", "w", encoding="utf8") as temp:
    json.dump(data, temp, ensure_ascii=False)
