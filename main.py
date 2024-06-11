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
    df_pl = read_with_polars(start_year=2014, end_year=2015, constants=constants, settings=settings)
    df_pjm = read_pjm_data(start_year=2014, end_year=2015, constants=constants, settings=settings)


    compute_daily_average_load(settings=settings, constants=constants, first_year=2012, last_year=2024)






    dummy = -32


if __name__ == '__main__':
    app_settings = Settings()
    print(f'{app_settings.APPLICATION_NAME} started at {datetime.datetime.now()}')
    time1 = time.time()
    main(settings=app_settings)
    time2 = time.time()
    print(f'{app_settings.APPLICATION_NAME} finished at {datetime.datetime.now()}')
    print(f'{app_settings.APPLICATION_NAME} took {(time2 - time1):.2f} seconds')
