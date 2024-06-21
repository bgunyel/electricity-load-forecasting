import datetime

import torch
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
        self.df_nerc = read_pjm_data(
            start_year=first_year,
            end_year=last_year,
            aggregation_level=constants.NERC_REGION
        ).to_pandas().set_index(keys=constants.LOCAL_DATE_TIME)
        self.df_mkt = read_pjm_data(
            start_year=first_year,
            end_year=last_year,
            aggregation_level=constants.MKT_REGION
        ).to_pandas().set_index(keys=constants.LOCAL_DATE_TIME)

        self.first_date_time = self.df_zone.index.min()
        self.last_date_time = self.first_date_time + datetime.timedelta(days=self.T) - datetime.timedelta(hours=1)
        self.next_date_time = self.first_date_time + datetime.timedelta(days=self.T)

    def next_batch(self):
        x = self.df_zone[self.first_date_time:self.next_date_time]
        y = self.df_zone[self.next_date_time:self.next_date_time+datetime.timedelta(hours=23)]

        self.first_date_time += datetime.timedelta(days=1)
        self.last_date_time += datetime.timedelta(days=1)
        self.next_date_time += datetime.timedelta(days=1)

        return x, y
