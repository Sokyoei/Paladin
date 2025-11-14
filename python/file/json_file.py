import json

try:
    import ujson  # https://github.com/ultrajson/ultrajson

    USE_UJSON = True
except ModuleNotFoundError:
    USE_UJSON = False

try:
    import orjson  # https://github.com/ijl/orjson

    USE_ORJSON = True
except ModuleNotFoundError:
    USE_ORJSON = False


from Ahri.Paladin import SOKYOEI_DATA_DIR

########################################################################################################################
# std json
########################################################################################################################
# json -> dict
with open(SOKYOEI_DATA_DIR / "Ahri/Ahri.json", "r", encoding="utf8") as Ahri:
    data = json.load(Ahri)
    print(data)

# dict -> json
with open("tempCodeRunnerFile.json", "w", encoding="utf8") as temp:
    json.dump(data, temp, ensure_ascii=False)

########################################################################################################################
# ujson
########################################################################################################################
if USE_UJSON:
    # json -> dict
    with open(SOKYOEI_DATA_DIR / "Ahri/Ahri.json", "r", encoding="utf8") as Ahri:
        data = ujson.load(Ahri)
        print(data)

    # dict -> json
    with open("tempCodeRunnerFile.json", "w", encoding="utf8") as temp:
        ujson.dump(data, temp, ensure_ascii=False)

########################################################################################################################
# orjson
########################################################################################################################
if USE_ORJSON:
    # json -> dict
    with open(SOKYOEI_DATA_DIR / "Ahri/Ahri.json", "rb") as Ahri:
        data = orjson.loads(Ahri.read())
        print(data)

    # dict -> json
    with open("tempCodeRunnerFile.json", "wb") as temp:
        temp.write(orjson.dumps(data))
