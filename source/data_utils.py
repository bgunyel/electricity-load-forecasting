import os
import datetime

import pandas as pd
import polars as pl

from config import Settings, Constants


def read_pjm_data(start_year: int, end_year: int, settings: Settings, constants: Constants) -> pl.DataFrame:
    if start_year > end_year:
        raise Exception("start_year must be less than or equal to end_year")

    file_path = os.path.join(settings.PJM_FOLDER, f'pjm-{start_year}.csv')
    out_df = pl.read_csv(source=file_path)

    for y in range(start_year + 1, end_year + 1):
        file_path = os.path.join(settings.PJM_FOLDER, f'pjm-{y}.csv')
        df = pl.read_csv(source=file_path)
        out_df = pl.concat(items=[out_df, df], how='vertical')

    out_df = out_df.with_columns(
        pl.col(constants.DATE_TIME_UTC).str.to_datetime(format="%m/%d/%Y %I:%M:%S %p"),
        pl.col(constants.DATE_TIME_EPT).str.to_datetime(format="%m/%d/%Y %I:%M:%S %p"),
    )

    # Local Date Time is assumed to be UTC-5 throughout the year
    # All the analyses will be carried with UTC-5 instead of UTC
    out_df = out_df.with_columns(
        pl.col(constants.DATE_TIME_UTC).dt.offset_by("-5h").alias(constants.LOCAL_DATE_TIME)
    )

    out_df = out_df.group_by(
        by=[constants.LOCAL_DATE_TIME, constants.ZONE],
        maintain_order=True
    ).agg(pl.sum(constants.LOAD))

    out_df = out_df.pivot(
        index=constants.LOCAL_DATE_TIME,
        columns=constants.ZONE,
        values=constants.LOAD,
        sort_columns=True
    )

    return out_df


def read_ghcnd_stations(country: str, settings: Settings, constants: Constants) -> pd.DataFrame:

    # df = pd.read_table(constants.GHCND_STATIONS)

    f = open(os.path.join(settings.GHCND_FOLDER, 'ghcnd-stations.txt'), "r")
    lines = f.readlines()
    f.close()

    q = [(t[0:11], t[38:40], float(t[12:20]), float(t[21:30]), float(t[31:37])) for t in lines if t[0:2] == country]
    df = pd.DataFrame(q, columns=[constants.ID, constants.STATE, constants.LAT, constants.LON, constants.ELEV])

    return df
