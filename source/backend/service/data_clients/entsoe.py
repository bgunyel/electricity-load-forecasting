import datetime

import requests
from lxml import objectify


class ENTSOEClient:
    def __init__(self, token):
        self.endpoint_url = 'https://web-api.tp.entsoe.eu/api'
        self.token = token

        self.eic_codes = {
            'AL': '10YAL-KESH-----5',  # Albania
            'AT': '10YAT-APG------L',  # Austria
            'BA': '10YBA-JPCC-----D',  # Bosnia & Herzegovina
            'BE': '10YBE----------2',  # Belgium
            'BG': '10YCA-BULGARIA-R',  # Bulgaria
            'CH': '10YCH-SWISSGRIDZ',  # Switzerland
            'CY': '10YCY-1001A0003J',  # Cyprus
            'CZ': '10YCZ-CEPS-----N',  # Czechia
            'DE': '10Y1001A1001A83F',  # Germany
            'DK': '10Y1001A1001A65H',  # Denmark
            'ES': '10YES-REE------0',  # Spain
            'FI': '10YFI-1--------U',  # Finland
            'FR': '10YFR-RTE------C',  # France
            'GE': '10Y1001A1001B012',  # Georgia
            'GR': '10YGR-HTSO-----Y',  # Greece
            'HR': '10YHR-HEP------M',  # Croatia
            'HU': '10YHU-MAVIR----U',  # Hungary
            'IE': '10YIE-1001A00010',  # Ireland
            'IT': '10YIT-GRTN-----B',  # Italy
            'LT': '10YLT-1001A0008Q',  # Lithuania
            'LU': '10YLU-CEGEDEL-NQ',  # Luxembourg
            'LV': '10YLV-1001A00074',  # Latvia
            'MD': '10Y1001A1001A990',  # Moldova
            'ME': '10YCS-CG-TSO---S',  # Montenegro
            'MK': '10YMK-MEPSO----8',  # North Macedonia
            'NL': '10YNL----------L',  # Netherlands
            'NO': '10YNO-0--------C',  # Norway
            'PL': '10YPL-AREA-----S',  # Poland
            'PT': '10YPT-REN------W',  # Portugal
            'RO': '10YRO-TEL------P',  # Romania
            'RS': '10YCS-SERBIATSOV',  # Serbia
            'SE': '10YSE-1--------K',  # Sweden
            'SI': '10YSI-ELES-----O',  # Slovenia
            'SK': '10YSK-SEPS-----K',  # Slovakia
            'XK': '10Y1001C--00100H',  # Kosovo
        }

        self.time_resolutions = {
            'PT15M': datetime.timedelta(minutes=15),
            'PT30M': datetime.timedelta(minutes=30),
            'PT60M': datetime.timedelta(hours=1),
        }

    def get_load_data(
            self,
            entity_code: str,
            start_datetime: datetime.datetime,
            end_datetime: datetime.datetime) -> list[dict]:

        format_str = "%Y%m%d%H%M"

        params = {
            'securityToken': self.token,
            'documentType': 'A65',
            'processType': 'A16',
            'outBiddingZone_Domain': self.eic_codes[entity_code],
            'periodStart': start_datetime.strftime(format=format_str),
            'periodEnd': end_datetime.strftime(format=format_str),
        }
        response = requests.get(url=self.endpoint_url, params=params)
        xml_text = response.text.encode('ascii')
        xml_doc = objectify.fromstring(xml_text)

        out_list = []

        if hasattr(xml_doc, 'TimeSeries'):
            for ts in xml_doc.TimeSeries:
                for period in ts.Period:
                    period_start = (
                        datetime.datetime.fromisoformat(period.timeInterval.start.text).astimezone(
                            datetime.timezone.utc
                        )
                    )
                    time_resolution = self.time_resolutions[period.resolution.text]
                    points = period.Point

                    for point in points:
                        position = int(point.position)
                        point_start = period_start + time_resolution * (position - 1)
                        point_end = period_start + time_resolution * position
                        point_value = int(point.quantity.text)
                        out_list.append(
                            {
                                'start_datetime': point_start,
                                'end_datetime': point_end,
                                'value': point_value,
                            }
                        )

        return out_list
