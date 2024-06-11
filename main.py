import os
import time
import datetime

import torch
import pandas as pd

from config import Settings, ModelSettings, Constants
from source.utils import compute_daily_average_load, read_pjm_data, read_with_polars


def main(settings: Settings):
    print(torch.__version__)
    if torch.cuda.is_available():
        print(f'CUDA Current Device: {torch.cuda.current_device()}')
    else:
        raise RuntimeError('No GPU found!')

    constants = Constants()
    model_settings = ModelSettings()

    ##
    start_year = 2012
    end_year = 2024

    time1 = time.time()
    df_pandas = read_pjm_data(start_year=start_year, end_year=end_year, constants=constants, settings=settings, read_package='pandas')
    time2 = time.time()
    df_polars = read_pjm_data(start_year=start_year, end_year=end_year, constants=constants, settings=settings, read_package='polars')
    time3 = time.time()

    print(f'Pandas Time: {time2 - time1}')
    print(f'Polars Time: {time3 - time2}')



    # compute_daily_average_load(settings=settings, constants=constants, first_year=2012, last_year=2024)






    dummy = -32


if __name__ == '__main__':
    app_settings = Settings()
    print(f'{app_settings.APPLICATION_NAME} started at {datetime.datetime.now()}')
    time1 = time.time()
    main(settings=app_settings)
    time2 = time.time()
    print(f'{app_settings.APPLICATION_NAME} finished at {datetime.datetime.now()}')
    print(f'{app_settings.APPLICATION_NAME} took {(time2 - time1):.2f} seconds')