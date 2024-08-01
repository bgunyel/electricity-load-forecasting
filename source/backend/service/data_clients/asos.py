import datetime
import os
import json
from urllib.request import urlopen


class ASOSClient:
    def __init__(self):

        self.service_url = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
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
