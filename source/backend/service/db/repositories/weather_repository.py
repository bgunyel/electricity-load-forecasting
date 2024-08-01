import datetime

from sqlalchemy.orm import Session
from sqlalchemy import insert, update, and_, or_

from backend.service.db.models.weather_station import WeatherStation
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

    def add_new_weather_stations(self, weather_stations: list[dict]):
        for station in weather_stations:
            station['created_at'] = station['created_at'].replace(microsecond=0)
            station['updated_at'] = station['updated_at'].replace(microsecond=0)
        self.__insert_weather_station(weather_stations=weather_stations)

