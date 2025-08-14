import pandas as pd

from Ahri.Paladin import SOKYOEI_DATA_DIR


def main():
    csv_path = SOKYOEI_DATA_DIR / "原神/原神.csv"
    genshin = pd.read_csv(csv_path, encoding="utf-8")
    print(genshin)


if __name__ == '__main__':
    main()
