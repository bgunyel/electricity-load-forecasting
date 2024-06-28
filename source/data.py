import datetime

import torch
import numpy as np
import polars as pl
import pandas as pd

from source.data_utils import read_pjm_data
from config import settings, constants


class PJMDataset:
    def __init__(self, B: int, T: int, first_year: int, last_year: int):
        self.B = B
        self.T = T

        self.first_year = first_year
        self.last_year = last_year

        self.df_zone = read_pjm_data(
            start_year=first_year,
            end_year=last_year,
            aggregation_level=constants.ZONE
        ).to_pandas().set_index(keys=constants.LOCAL_DATE_TIME)

        self.df_zone_availability = self.df_zone.notna().drop(columns=['RTO'])

        self.x_date_time_open = self.df_zone.index.min()
        self.x_date_time_close = self.x_date_time_open + datetime.timedelta(days=self.T) - datetime.timedelta(hours=1)
        self.y_date_time_open = self.x_date_time_open + datetime.timedelta(days=self.T)
        self.y_date_time_close = self.y_date_time_open + datetime.timedelta(hours=23)

    def next_batch(self):
        x = self.df_zone[self.x_date_time_open:self.x_date_time_close]
        y = self.df_zone[self.y_date_time_open:self.y_date_time_close]

        zone_availability = self.df_zone_availability[self.x_date_time_open: self.y_date_time_close].agg(lambda t: sum(t) == (self.T+1)*24)
        available_zones = [i for i in zone_availability.index if zone_availability[i]]
        new_indices = np.random.randint(low=0, high=len(available_zones), size=self.B - len(available_zones))
        available_zones += [available_zones[t] for t in new_indices]

        a = x[available_zones]
        b = a.to_numpy()

        x = x[available_zones]
        y = y[available_zones]

        self.x_date_time_open += datetime.timedelta(days=1)
        self.x_date_time_close += datetime.timedelta(days=1)
        self.y_date_time_open += datetime.timedelta(days=1)
        self.y_date_time_close += datetime.timedelta(days=1)

        return x, y
