"""
读取 PrepBUFR 观测数据
"""

import platform
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

if platform.system() == "Windows":
    raise SystemError("necpbufr not support Windows")

import ncepbufr


def read_prepbufr(bufr_path):
    # hdstr = "SID XOB YOB DHR TYP ELV SAID T29"
    # obstr = "POB QOB TOB ZOB UOB VOB PWO CAT PRSS"
    # qcstr = "PQM QQM TQM ZQM WQM NUL PWQ     "
    # oestr = "POE QOE TOE NUL WOE NUL PWE     "

    hdstr = "SID XOB YOB DHR"
    obstr = "POB QOB TOB UOB VOB"

    data = []
    bufr = ncepbufr.open(bufr_path)
    while bufr.advance() == 0:  # loop over messages.
        if bufr.msg_type == "ADPSFC":
            print(bufr.msg_counter, bufr.msg_type, bufr.msg_date, bufr.receipt_time)
            while bufr.load_subset() == 0:  # loop over subsets in message.
                hdr = bufr.read_subset(hdstr).filled(np.nan).squeeze()
                station_id = bytes(hdr[0]).decode().strip()  # .tostring()
                obs = bufr.read_subset(obstr).filled(np.nan).squeeze()
                # 忽略没有经纬度的数据
                if hdr[1] == np.nan and hdr[2] == np.nan:
                    continue
                # 忽略南半球数据
                if hdr[2] < 0:
                    continue
                data.append(
                    [
                        station_id,
                        float(hdr[1]),
                        float(hdr[2]),
                        (datetime.strptime(str(bufr.msg_date), "%Y%m%d%H") + timedelta(hours=hdr[3])).strftime(
                            "%Y%m%d%H"
                        ),
                        float(obs[0]),
                        float(obs[1]),
                        float(obs[2]),
                        float(obs[3]),
                        float(obs[4]),
                    ]
                )
    bufr.close()
    return pd.DataFrame(data, columns=["ID", "Lon", "Lat", "DateTime", "P", "Q", "T", "U", "V"])


def main():
    read_prepbufr("gdas.t00z.prepbufr.nr")


if __name__ == "__main__":
    main()
