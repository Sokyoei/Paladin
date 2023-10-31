import json

# json -> dict
with open("../../data/Ahri/Ahri.json", "r", encoding="utf8") as Ahri:
    data = json.load(Ahri)
    print(data)

# dict -> json
with open("tempCodeRunnerFile.json", "w", encoding="utf8") as w:
    json.dump(data, w, ensure_ascii=False)
