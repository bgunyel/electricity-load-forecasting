from backend.service.db.models.weather_data import WeatherData
from backend.service.db.models.weather_station import WeatherStation
from backend.service.db.entities.weather_entities import WeatherStationEntity, WeatherDataEntity


def weather_station_model_to_entity(instance: WeatherStation) -> WeatherStationEntity:
    return WeatherStationEntity(
        id=instance.id,
        code=instance.code,
        name=instance.name,
        geographical_unit_id=instance.geographical_unit_id,
        longitude=instance.longitude,
        latitude=instance.latitude,
        elevation=instance.elevation,
        is_active=instance.is_active,
        archive_begin=instance.archive_begin,
        archive_end=instance.archive_end,
        last_valid_data_ending=instance.last_valid_data_ending,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
        created_by_id=instance.created_by_id,
        updated_by_id=instance.updated_by_id
    )


def weather_data_model_to_entity(instance: WeatherData) -> WeatherDataEntity:
    return WeatherDataEntity(
        id=instance.id,
        station_id=instance.station_id,
        measured_at=instance.measured_at,
        temperature_celsius=instance.temperature_celsius,
        dewpoint_celsius=instance.dewpoint_celsius,
        relative_humidity=instance.relative_humidity,
        wind_direction=instance.wind_direction,
        wind_speed=instance.wind_speed,
        pressure_altimeter=instance.pressure_altimeter,
        feel_celsius=instance.feel_celsius,
        created_by_id=instance.created_by_id,
        updated_by_id=instance.updated_by_id,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
    )
