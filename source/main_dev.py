import os
import time
import datetime

import torch
import pandas as pd
import polars as pl

from config import settings, model_settings, pjm, entsoe
from source.backend.api import *
from source.backend.service.data_clients.entsoe import ENTSOEClient


def main():
    print(torch.__version__)
    if torch.cuda.is_available():
        print(f'CUDA Current Device: {torch.cuda.current_device()}')
    else:
        raise RuntimeError('No GPU found!')

    ##
    update_geographical_unit(
        code=GeographicalUnitCode.TURKIYE,
        last_valid_data_ending=datetime.datetime(year=2015, month=1, day=1, hour=0, minute=0,
                                                 tzinfo=datetime.timezone.utc)
    )

    ##
    entsoe_client = ENTSOEClient(token=settings.ENTSOE_TOKEN)

    entity_code = 'AT'
    start_datetime = datetime.datetime(year=2015, month=1, day=1, hour=0, minute=0, tzinfo=datetime.timezone.utc)
    end_datetime = datetime.datetime(year=2016, month=1, day=1, hour=0, minute=0, tzinfo=datetime.timezone.utc)
    # end_datetime = datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)

    t1 = time.time()
    data_list = entsoe_client.get_load_data(entity_code=entity_code,
                                            start_datetime=start_datetime,
                                            end_datetime=end_datetime)
    t2 = time.time()
    total_time = t2 - t1
    print(f'Total time: {total_time}')
    print(f'Time per element: {total_time / len(data_list)}')
    print(f'Number of elements: {len(data_list)}')
    dummy = -32


if __name__ == '__main__':
    print(f'{settings.APPLICATION_NAME} started at {datetime.datetime.now()}')
    time1 = time.time()
    main()
    time2 = time.time()
    print(f'{settings.APPLICATION_NAME} finished at {datetime.datetime.now()}')
    print(f'{settings.APPLICATION_NAME} took {(time2 - time1):.2f} seconds')
