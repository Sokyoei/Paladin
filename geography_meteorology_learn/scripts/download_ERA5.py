"""
download ERA5 datasets

https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset

Requires:
    create $HOME/.cdsapirc

    ```.cdsapirc
    url: https://cds.climate.copernicus.eu/api/v2
    key: {UID}:{API Key}
    ```

Warnings:
    ERA5 datasets has GRIB1 and GRIB2 mixed formatted.

Reference:
    https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation#heading-Parameterlistings
"""

from concurrent.futures import ProcessPoolExecutor
from typing import Literal

import cdsapi

c = cdsapi.Client()

TIMES = [
    # '00:00',
    # '01:00',
    # '02:00',
    # '03:00',
    # '04:00',
    # '05:00',
    # '06:00',
    # '07:00',
    # '08:00',
    # '09:00',
    # '10:00',
    # '11:00',
    '12:00',
    '13:00',
    '14:00',
    '15:00',
    '16:00',
    '17:00',
    '18:00',
    '19:00',
    '20:00',
    '21:00',
    '22:00',
    '23:00',
]


def download(year: str, month: str, day: str, time: str, data_type: Literal["grib", "netcdf"] = "grib"):
    suffix = {"grib": "grib", "netcdf": "nc"}.get(data_type)
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': format,
            'variable': ["temperature", "u_component_of_wind", "v_component_of_wind", "specific_rain_water_content"],
            'pressure_level': ["1000"],
            # 'pressure_level': [
            #     # fmt:off
            #     '1', '2', '3', '5', '7', '10', '20', '30', '50', '70', '100','125', '150', '175', '200', '225', '250',
            #     '300', '350', '400', '450', '500', '550', '600', '650', '700', '750', '775', '800', '825', '850', '875',
            #     '900', '925', '950', '975', '1000',
            #     # fmt:on
            # ],
            'year': year,
            'month': month,
            'day': day,
            'time': [time],
            'area': [24, 111, 20, 115],
        },
        # f'ERA5.pressure.{year:0>4}{month:0>2}{day:0>2}{time.replace(":", ""):0>2}.{suffix}',
        f'ERA5.pressure.1000hPa.{suffix}',
    )

    # c.retrieve(
    #     'reanalysis-era5-single-levels',
    #     {
    #         'product_type': 'reanalysis',
    #         'format': 'grib',
    #         'variable': "all",
    #         'pressure_level': 'all',
    #         'year': year,
    #         'month': month,
    #         'day': day,
    #         'time': [time],
    #         'area': [24, 111, 20, 115],
    #     },
    #     f'ERA5.single.{year:0>4}{month:0>2}{day:0>2}{time.replace(":", ""):0>2}.{suffix}',
    #     f'ERA5.single.{suffix}',
    # )


def main():
    with ProcessPoolExecutor(max_workers=16) as pp:
        for t in TIMES:
            pp.submit(download, "2024", "05", "08", t, "netcdf")
        pp.submit(download, "2024", "05", "09", "00:00", "netcdf")
        # pp.submit(download, "2024", "05", ["08", "09"], "all", "netcdf")


if __name__ == '__main__':
    main()
