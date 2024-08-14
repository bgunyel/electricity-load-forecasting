import datetime

from sqlalchemy.orm import Session
from sqlalchemy import insert, update, and_
from sqlalchemy.exc import DBAPIError

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
        try:
            self.session.execute(
                insert(WeatherData),
                weather_data
            )
        except DBAPIError as e:
            self.session.rollback()
            raise e
        else:
            self.session.commit()

    def add_new_weather_stations(self, weather_stations: list[dict]):
        for station in weather_stations:
            station['created_at'] = station['created_at'].replace(microsecond=0)
            station['updated_at'] = station['updated_at'].replace(microsecond=0)

        try:
            self.__insert_weather_station(weather_stations=weather_stations)
        except DBAPIError as e:
            print(f'DBAPIError: {e}')
            raise e

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

        try:
            self.__insert_weather_data(weather_data=weather_data)
        except DBAPIError as e:
            print(f'DBAPIError: {e}')
            raise e

    def get_weather_stations_from_geo_code_id(self, geo_unit_id: int) -> list[WeatherStationEntity]:
        query_result = (
            self.session.query(WeatherStation)
            .where(
                and_(
                    WeatherStation.geographical_unit_id.__eq__(geo_unit_id),
                    WeatherStation.is_active.__eq__(True),
                )
            )
            .order_by(WeatherStation.name)
        )
        stations = [weather_station_model_to_entity(instance=x) for x in query_result]
        return stations

    def update_weather_station(self, id: int, update_dict: dict):
        self.session.execute(
            update(WeatherStation)
            .where(
                WeatherStation.id.__eq__(id)
            )
            .values(update_dict)
        )
        self.session.commit()
