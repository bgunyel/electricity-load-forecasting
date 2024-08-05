import datetime
import time

import torch

from config import settings
from source.backend.api import *


def main():
    print(torch.__version__)
    if torch.cuda.is_available():
        print(f'CUDA Current Device: {torch.cuda.current_device()}')
    else:
        raise RuntimeError('No GPU found!')

    ##


    """
    asos_client = ASOSClient()
    data_list = asos_client.get_weather_data(station_code='LTAC',
                                             start_date=datetime.date(year=2015, month=1, day=1),
                                             end_date=datetime.date(year=2024, month=8, day=4))

    """


    # sync_all_data()
    sync_weather_data(geo_unit_code=GeographicalUnitCode.NETHERLANDS, regulator=RegulatorType.ENTSOE)


    # fetch_and_add_weather_stations(code=GeographicalUnitCode.SWITZERLAND, regulator=RegulatorType.ENTSOE)

    dummy = -32

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
