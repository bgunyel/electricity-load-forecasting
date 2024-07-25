import enum


class GeographicalUnitType(enum.Enum):
    COUNTRY = 'Country'
    CONTROL_AREA = 'Control Area'
    BIDDING_ZONE = 'Bidding Zone'


class RegulatorType(enum.Enum):
    ENTSOE = 'ENTSOE'
    EPIAS = 'EPIAS'
    PJM = 'PJM'


class GeographicalUnitCode(enum.Enum):
    AUSTRIA = 'AT'
    BELGIUM = 'BE'
    GERMANY = 'DE'
    TURKIYE = 'TR'
