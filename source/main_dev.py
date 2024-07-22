import os
import time
import datetime

import torch
import pandas as pd
import polars as pl

from config import settings, model_settings, pjm, entsoe
from source.backend.data_clients.entsoe import ENTSOEClient


def main():
    print(torch.__version__)
    if torch.cuda.is_available():
        print(f'CUDA Current Device: {torch.cuda.current_device()}')
    else:
        raise RuntimeError('No GPU found!')

    ##

    entsoe_client = ENTSOEClient(token=settings.ENTSOE_TOKEN)

    entity_code = 'AT'
    start_datetime = datetime.datetime(year=2024, month=7, day=19, hour=0, minute=0, tzinfo=datetime.timezone.utc)
    end_datetime = datetime.datetime(year=2024, month=7, day=20, hour=0, minute=0, tzinfo=datetime.timezone.utc)

    entsoe_client.get_load_data(entity_code=entity_code, start_datetime=start_datetime, end_datetime=end_datetime)

    dummy = -32


if __name__ == '__main__':
    print(f'{settings.APPLICATION_NAME} started at {datetime.datetime.now()}')
    time1 = time.time()
    main()
    time2 = time.time()
    print(f'{settings.APPLICATION_NAME} finished at {datetime.datetime.now()}')
    print(f'{settings.APPLICATION_NAME} took {(time2 - time1):.2f} seconds')
