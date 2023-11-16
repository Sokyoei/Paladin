import csv

import numpy as np
import pandas as pd

csv_file_path = r"../../data/原神/原神.csv"

from_pd = pd.read_csv(csv_file_path, encoding="utf8")
print(from_pd)

# 无法处理 null
from_np = np.loadtxt(csv_file_path, encoding="utf8", dtype=str, delimiter=",", skiprows=1)
print(from_np)
