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
    BOSNIA_HERZEGOVINA = 'BA'
    CROATIA = 'HR'
    CZECHIA = 'CZ'
    DENMARK = 'DK'
    ESTONIA = 'EE'
    FINLAND = 'FI'
    FRANCE = 'FR'
    GERMANY = 'DE'
    GREECE = 'GR'
    HUNGARY = 'HU'
    IRELAND = 'IE'
    ITALY = 'IT'
    KOSOVO = 'XK'
    LATVIA = 'LV'
    LITHUANIA = 'LT'
    LUXEMBOURG = 'LU'
    MOLDOVA = 'MD'
    MONTENEGRO = 'ME'
    NETHERLANDS = 'NL'
    NORTH_MACEDONIA = 'MK'
    NORWAY = 'NO'
    POLAND = 'PL'
    PORTUGAL = 'PT'
    ROMANIA = 'RO'
    SERBIA = 'RS'
    SLOVAKIA = 'SK'
    SLOVENIA = 'SI'
    SPAIN = 'ES'
    SWEDEN = 'SE'
    SWITZERLAND = 'CH'
    TURKIYE = 'TR'
