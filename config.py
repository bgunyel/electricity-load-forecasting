import os
from pydantic_settings import BaseSettings

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    APPLICATION_NAME: str = "Electricity Load Forecasting"

    EPIAS_FOLDER: str
    PJM_FOLDER: str
    GHCND_FOLDER: str
    PJM_GHCND_FOLDER: str
    OUT_FOLDER: str

    WATT_TIME_USER: str
    WATT_TIME_PASS: str

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
        env_file = os.path.join(ROOT_DIR, '.env')


class Constants(BaseSettings):
    PJM_STATES: list = ['DE', 'IL', 'IN', 'KY', 'MD', 'MI', 'NJ', 'NC', 'OH', 'PA', 'TN', 'VA', 'WV', 'DC']
    PJM_ZONES: list = ['AE', 'AEP', 'AP', 'ATSI', 'BC', 'CE', 'CNCT', 'DAY', 'DEOK', 'DOM', 'DPL', 'DUQ', 'EKPC',
                       'GPU', 'JC', 'ME', 'OVEC', 'PE', 'PEP', 'PL', 'PN', 'PS', 'RECO']  # RTO excluded from the list
    PJM_LOAD_AREAS: list = ['AE', 'AECO', 'AEP', 'AEPAPT', 'AEPIMP', 'AEPKPT', 'AEPOPT', 'AP', 'BC', 'CE',
                            'DAY', 'DEOK', 'DOM', 'DPL', 'DPLCO', 'DUQ', 'EASTON', 'EKPC', 'JC', 'ME', 'OE', 'OVEC',
                            'PAPWR', 'PE', 'PEP', 'PEPCO', 'PLCO', 'PN', 'PS', 'RECO', 'RTO', 'SMECO', 'UGI', 'VMEU']

    MKT_REGIONS: list = ['MIDATL', 'SOUTH', 'WEST']  # RTO excluded from the list
    NERC_REGIONS: list = ['RFC', 'SERC']  # RTO excluded from the list

    NERC_REGION: str = 'nerc_region'
    MKT_REGION: str = 'mkt_region'
    ZONE: str = 'zone'
    LOAD_AREA: str = 'load_area'

    AGGREGATION_MAP: dict = {
        NERC_REGION: NERC_REGIONS,
        MKT_REGION: MKT_REGIONS,
        ZONE: PJM_ZONES,
        LOAD_AREA: PJM_LOAD_AREAS
    }

    DATE_TIME_UTC: str = 'datetime_beginning_utc'
    DATE_TIME_EPT: str = 'datetime_beginning_ept'
    LOAD: str = 'mw'
    IS_VERIFIED: str = 'is_verified'
    LOCAL_DATE_TIME: str = 'local_date_time'
    HOUR: str = 'hour'

    ID: str = 'id'
    STATE: str = 'state'
    LAT: str = 'latitude'
    LON: str = 'longitude'
    ELEV: str = 'elevation'
    STATE_ID: str = 'state_id'
    REGION: str = 'region'


class ModelSettings(BaseSettings):
    device: str = "cuda"


settings = Settings()
constants = Constants()
model_settings = ModelSettings()
