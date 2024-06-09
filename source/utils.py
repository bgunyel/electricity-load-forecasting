import os
import pandas as pd

from config import Settings, Constants


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

