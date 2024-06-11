import os
from pydantic_settings import BaseSettings

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    APPLICATION_NAME: str = "Electricity Load Forecasting"

    EPIAS_FOLDER: str
    PJM_FOLDER: str
    GHCND_FOLDER: str
    OUT_FOLDER: str

    WATT_TIME_USER: str
    WATT_TIME_PASS: str

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
        env_file = os.path.join(ROOT_DIR, '.env')


class Constants(BaseSettings):

    PJM_STATES: list = ['DE', 'IL', 'IN', 'KY', 'MD', 'MI', 'NJ', 'NC', 'OH', 'PA', 'TN', 'VA', 'WV', 'DC']
    DATE_TIME_UTC: str = 'datetime_beginning_utc'
    DATE_TIME_EPT: str = 'datetime_beginning_ept'
    NERC_REGION: str = 'nerc_region'
    MKT_REGION: str = 'mkt_region'
    ZONE: str = 'zone'
    LOAD_AREA: str = 'load_area'
    LOAD: str = 'mw'
    IS_VERIFIED: str = 'is_verified'
    LOCAL_DATE_TIME: str = 'local_date_time'


class ModelSettings(BaseSettings):
    device: str = "cuda"
