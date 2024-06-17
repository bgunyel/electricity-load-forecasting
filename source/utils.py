import os
import datetime

import pandas as pd
import polars as pl
import matplotlib.pyplot as plt

from config import Settings, Constants


def read_pjm_data(
        start_year: int,
        end_year: int,
        settings: Settings,
        constants: Constants,
        read_package: str = 'polars'
) -> [pd.DataFrame, pl.DataFrame]:
    match read_package:
        case 'pandas':
            out_df = read_with_pandas(start_year=start_year, end_year=end_year, settings=settings, constants=constants)
        case 'polars':
            out_df = read_with_polars(start_year=start_year, end_year=end_year, settings=settings, constants=constants)
        case _:
            raise Exception('Undefined!')

    return out_df


def read_with_pandas(start_year: int, end_year: int, settings: Settings, constants: Constants) -> pd.DataFrame:
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


def compute_daily_average_load(
        settings: Settings,
        constants: Constants,
        first_year: int = 2012,
        last_year: int = 2024):
    for idx, year in enumerate(range(first_year, last_year + 1)):

        df = read_pjm_data(start_year=year, end_year=year, settings=settings, constants=constants)
        df = df.with_columns(
            pl.col(constants.LOCAL_DATE_TIME).dt.hour().alias(constants.HOUR)
        )
        active_zones = [x for x in df.columns if x in constants.PJM_ZONES]
        grouped_df = df.group_by(by=constants.HOUR, maintain_order=True).agg(pl.mean(active_zones))

        plt.figure(figsize=(18, 8))

        for zone in active_zones:
            plt.plot(grouped_df[constants.HOUR], grouped_df[zone], label=zone)

        plt.title(label=f'{year}')
        plt.grid(visible=True)
        plt.legend()
        plt.xlabel('Hour (UTC-5)')
        plt.ylabel('Average Load (MW)')
        plt.show()


def box_plots_for_zones(
        settings: Settings,
        constants: Constants,
        first_year: int = 2012,
        last_year: int = 2024):
    load_dict = {z: dict() for z in constants.PJM_ZONES}
    load_dict['RTO'] = dict()

    for idx, year in enumerate(range(first_year, last_year + 1)):
        df = read_pjm_data(start_year=year, end_year=year, settings=settings, constants=constants)
        active_zones = [x for x in df.columns if x in constants.PJM_ZONES]

        load_dict['RTO'][year] = df['RTO']
        for zone in active_zones:
            load_dict[zone][year] = df[zone]

    dummy = -32

    for zone in constants.PJM_ZONES + ['RTO']:
        plt.figure(figsize=(18, 8))
        x = [[v for v in list(load_dict[zone][y]) if v is not None] for y in load_dict[zone].keys()]
        plt.boxplot(x=x)
        labels = list(load_dict[zone].keys())
        plt.xticks(range(1, len(labels) + 1), labels)
        # plt.boxplot(x=load_dict[zone], label=list(load_dict[zone].keys()))
        plt.title(label=f'{zone}')
        plt.grid(visible=True)
        # plt.legend()
        plt.xlabel('Year')
        plt.ylabel('Load (MW)')
        plt.show()

    dummy = -43
