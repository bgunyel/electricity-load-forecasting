import os
import time
import datetime

import torch
import pandas as pd
import polars as pl

from config import settings, model_settings, pjm, entsoe
from source.backend.api import *
from source.backend.service.data_clients.entsoe import ENTSOEClient
from backend.service.utils.get_db_session import get_db_session
from backend.service.db.repositories.load_data_repository import LoadDataRepository


def main():
    print(torch.__version__)
    if torch.cuda.is_available():
        print(f'CUDA Current Device: {torch.cuda.current_device()}')
    else:
        raise RuntimeError('No GPU found!')

    ##
    sync_all_data()
    # sync_load_data(entity_code=GeographicalUnitCode.BOSNIA_HERZEGOVINA, regulator=RegulatorType.ENTSOE)

    """
    for geo_code in GeographicalUnitCode:
        if geo_code in [GeographicalUnitCode.TURKIYE, GeographicalUnitCode.AUSTRIA, GeographicalUnitCode.BELGIUM]:
            continue

        update_geographical_unit(
            code=geo_code,
            regulator=RegulatorType.ENTSOE,
            last_valid_data_ending=None
        )
    """





    dummy = -32


if __name__ == '__main__':
    print(f'{settings.APPLICATION_NAME} started at {datetime.datetime.now()}')
    time1 = time.time()
    main()
    time2 = time.time()
    print(f'{settings.APPLICATION_NAME} finished at {datetime.datetime.now()}')
    print(f'{settings.APPLICATION_NAME} took {(time2 - time1):.2f} seconds')
