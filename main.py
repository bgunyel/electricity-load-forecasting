import os
import time
import datetime

import torch
import pandas as pd
import polars as pl

from config import settings, constants, model_settings
from source.utils import box_plots_for_zones
from source.data_utils import read_pjm_data
from source.map_utils import visualize_stations, visualize_pjm_stations, get_pjm_regions_for_weather_stations
from source.data import PJMDataset


def main():
    print(torch.__version__)
    if torch.cuda.is_available():
        print(f'CUDA Current Device: {torch.cuda.current_device()}')
    else:
        raise RuntimeError('No GPU found!')

    ##
    pjm_data_set = PJMDataset(first_year=2012, last_year=2024, B=20, T=4)

    for i in range(10):
        x, y = pjm_data_set.next_batch()
        print(f'{x.index.min()} - {x.index.max()} --- {y.index.min()} - {y.index.max()}')
        dummy = -32


    dummy = -32


if __name__ == '__main__':
    print(f'{settings.APPLICATION_NAME} started at {datetime.datetime.now()}')
    time1 = time.time()
    main()
    time2 = time.time()
    print(f'{settings.APPLICATION_NAME} finished at {datetime.datetime.now()}')
    print(f'{settings.APPLICATION_NAME} took {(time2 - time1):.2f} seconds')
