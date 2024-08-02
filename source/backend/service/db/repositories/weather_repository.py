import datetime

from sqlalchemy.orm import Session
from sqlalchemy import insert, update, and_, or_

from backend.service.db.models.weather_station import WeatherStation
from backend.service.db.models.weather_data import WeatherData
from backend.service.db.entities.weather_entities import WeatherStationEntity
from backend.service.db.data_mappers.weather_data_mappers import weather_station_model_to_entity


class WeatherRepository:
    def __init__(self, session: Session):
        self.session = session

    def __insert_weather_station(self, weather_stations: list[dict]):
        self.session.execute(
            insert(WeatherStation),
            weather_stations
        )
        self.session.commit()

    def __insert_weather_data(self, weather_data: [dict, list[dict]]):
        self.session.execute(
            insert(WeatherData),
            weather_data
        )
        self.session.commit()

    def add_new_weather_stations(self, weather_stations: list[dict]):
        for station in weather_stations:
            station['created_at'] = station['created_at'].replace(microsecond=0)
            station['updated_at'] = station['updated_at'].replace(microsecond=0)
        self.__insert_weather_station(weather_stations=weather_stations)

    def add_new_weather_data(self, weather_data: list[dict]):
        # TODO: Safety checks shall be implemented
        # Updates weather_data (list) in-place
        _ = [
            x.update(
                {
                    'measured_at': x['measured_at'].replace(microsecond=0),
                    'created_at': x['created_at'].replace(microsecond=0),
                    'updated_at': x['updated_at'].replace(microsecond=0),
                }
            ) for x in weather_data
        ]
        self.__insert_weather_data(weather_data=weather_data)
