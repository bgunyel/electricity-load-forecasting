import os
import time
import datetime

import torch
import pandas as pd

from config import settings, constants, model_settings
from source.utils import box_plots_for_zones
from source.data_utils import read_pjm_data
from source.map_utils import visualize_stations, visualize_pjm_stations, get_regions_of_ghcnd_stations_from_watt_time


def main():
    print(torch.__version__)
    if torch.cuda.is_available():
        print(f'CUDA Current Device: {torch.cuda.current_device()}')
    else:
        raise RuntimeError('No GPU found!')



    ##
    get_regions_of_ghcnd_stations_from_watt_time()




    dummy = -32


if __name__ == '__main__':

    print(f'{settings.APPLICATION_NAME} started at {datetime.datetime.now()}')
    time1 = time.time()
    main()
    time2 = time.time()
    print(f'{settings.APPLICATION_NAME} finished at {datetime.datetime.now()}')
    print(f'{settings.APPLICATION_NAME} took {(time2 - time1):.2f} seconds')
