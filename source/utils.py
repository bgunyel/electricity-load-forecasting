import os
import datetime

import pandas as pd
import polars as pl

from config import Settings, Constants


def read_pjm_data(start_year: int, end_year: int, settings: Settings, constants: Constants) -> pd.DataFrame:

    if start_year > end_year:
        raise Exception("start_year must be less than or equal to end_year")

    file_path = os.path.join(settings.PJM_FOLDER, f'pjm-{start_year}.csv')
    out_df = pd.read_csv(file_path)

    for y in range(start_year + 1, end_year + 1):
        file_path = os.path.join(settings.PJM_FOLDER, f'pjm-{y}.csv')
        df = pd.read_csv(file_path)
        out_df = pd.concat(objs=[out_df, df], axis=0, join='outer')

    out_df[constants.DATE_TIME_UTC] = out_df[constants.DATE_TIME_UTC].apply(
        lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p')
    )
    out_df[constants.DATE_TIME_EPT] = out_df[constants.DATE_TIME_EPT].apply(
        lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p')
    )
    # Local Date Time is assumed to be UTC-5 throughout the year
    # All the analyses will be carried with UTC-5 instead of UTC
    out_df[constants.LOCAL_DATE_TIME] = out_df[constants.DATE_TIME_UTC] - datetime.timedelta(hours=5)

    # Zone Level Aggregation
    out_df = out_df.groupby(
        by=[constants.LOCAL_DATE_TIME, constants.ZONE],
        as_index=False
    ).agg(
        **{
            constants.LOAD: pd.NamedAgg(column=constants.LOAD, aggfunc="sum")
        }
    )

    out_df = out_df.pivot(index=constants.LOCAL_DATE_TIME, columns=constants.ZONE, values=constants.LOAD)

    return out_df


def read_with_polars(start_year: int, end_year: int, settings: Settings, constants: Constants) -> pl.DataFrame:
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
    out_df = out_df.with_columns(
        pl.col(constants.DATE_TIME_UTC).dt.offset_by("-5h").alias(constants.LOCAL_DATE_TIME)
    )

    TODO: Here I am!

    dummy = -32



def compute_daily_average_load(
        settings: Settings,
        constants: Constants,
        first_year: int = 2012,
        last_year: int = 2024):
    file_path = os.path.join(settings.PJM_FOLDER, f'pjm-{last_year}.csv')
    df = pd.read_csv(file_path)
    active_zones = sorted(df[constants.ZONE].unique())

    for zone in active_zones:
        temp = df[df[constants.ZONE] == zone].groupby(by=constants.DATE_TIME_UTC)[constants.LOAD].mean()
        dummy = -43

    dummy = -32

