import matplotlib.pyplot as plt
import polars as pl

from config import settings, constants
from source.data_utils import read_pjm_data


def compute_daily_average_load(
        first_year: int = 2012,
        last_year: int = 2024
):
    for idx, year in enumerate(range(first_year, last_year + 1)):

        df = read_pjm_data(start_year=year, end_year=year)
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
        first_year: int = 2012,
        last_year: int = 2024
):
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
