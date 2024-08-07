import datetime
import os
import io
import json
from urllib.request import urlopen

import requests
import pandas as pd
import numpy as np



class ASOSClient:
    def __init__(self):

        self.service_url = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
        self.network_url = "https://mesonet.agron.iastate.edu/geojson/network/"

    def get_stations_for_network(self, country_code: str, state_code: str = None):

        network_code = None
        if country_code == 'US':
            if state_code is None:
                raise RuntimeError('State code can NOT be None for country code US')
            network_code = f'{state_code}_ASOS'
        else:
            network_code = f'{country_code}__ASOS'

        data = urlopen(os.path.join(self.network_url, f'{network_code}.geojson'))
        jdict = json.load(data)

        stations = []

        for item in jdict['features']:
            station = {
                'code': item['properties']['sid'],
                'name': item['properties']['sname'],
                'longitude': item['geometry']['coordinates'][0],
                'latitude': item['geometry']['coordinates'][1],
                'elevation': item['properties']['elevation'],
                'is_active': item['properties']['online'],
                'archive_begin': datetime.date.fromisoformat(
                    item['properties']['archive_begin']
                ) if item['properties']['archive_begin'] is not None else None,
                'archive_end': datetime.date.fromisoformat(
                    item['properties']['archive_end']
                ) if item['properties']['archive_end'] is not None else None,
            }
            stations.append(station)

        return stations

    def get_weather_data(self, station_code: str, start_date: datetime.date, end_date: datetime.date) -> list[dict]:

        params = {
            'station': station_code,
            'year1': str(start_date.year),
            'month1': str(start_date.month),
            'day1': str(start_date.day),
            'year2': str(end_date.year),
            'month2': str(end_date.month),
            'day2': str(end_date.day),
            'tz': 'UTC',
            'data': ['tmpc', 'dwpc', 'relh', 'drct', 'sknt', 'alti', 'feel'],
            'format': 'onlycomma',
            'latlon': 'no',
            'elev': 'no',
            'missing': 'null',
            'trace': 'T',
            'direct': 'no',
            'report_type': [3, 4]
        }
        response = requests.get(url=self.service_url, params=params)
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

        if 'feel' in df.columns:
            df['feel_celsius'] = (df['feel'] - 32) / 1.8  # Fahrenheit to Celsius
            df = df.drop(columns=['feel'])
        else:
            df['feel_celsius'] = np.nan

        df = df.drop(columns=['station'])
        df = df.rename(columns={'valid': 'measured_at',
                                'tmpc': 'temperature_celsius',
                                'dwpc': 'dewpoint_celsius',
                                'relh': 'relative_humidity',
                                'drct': 'wind_direction',
                                'sknt': 'wind_speed',
                                'alti': 'pressure_altimeter'})
        out_list = df.to_dict('records')
        return out_list



