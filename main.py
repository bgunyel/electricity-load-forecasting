import os
import time
import datetime

import torch
import pandas as pd

from config import Settings, ModelSettings, Constants
from source.utils import box_plots_for_zones
from source.data_utils import read_ghcnd_stations
from source.map_utils import visualize_stations, visualize_pjm_stations


def main(settings: Settings):
    print(torch.__version__)
    if torch.cuda.is_available():
        print(f'CUDA Current Device: {torch.cuda.current_device()}')
    else:
        raise RuntimeError('No GPU found!')

    constants = Constants()
    model_settings = ModelSettings()

    ##
    # visualize_pjm_stations(settings=settings, constants=constants)








    dummy = -32


if __name__ == '__main__':
    app_settings = Settings()
    print(f'{app_settings.APPLICATION_NAME} started at {datetime.datetime.now()}')
    time1 = time.time()
    main(settings=app_settings)
    time2 = time.time()
    print(f'{app_settings.APPLICATION_NAME} finished at {datetime.datetime.now()}')
    print(f'{app_settings.APPLICATION_NAME} took {(time2 - time1):.2f} seconds')
