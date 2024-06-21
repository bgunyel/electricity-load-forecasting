import os
import datetime
import time

import branca
import folium
import pandas as pd

import requests
from requests.auth import HTTPBasicAuth

from config import settings, constants
from source.data_utils import read_ghcnd_stations, get_watt_time_token


def draw_circles_on_map(
        vis_map: folium.Map,
        coordinates: list[tuple],
        circle_strengths: [list[float], list[int]],
        pop_up_text: list[str]):
    colors = ['#0000FF', '#4169E1', '#8A2BE2', '#4B0082', '#483D8B', '#6A5ACD', '#7B68EE', '#9370DB', '#9400D3',
              '#9932CC', '#BA55D3', '#800080', '#C71585', '#FF00FF', '#FF1493', '#F08080', '#FA8072', '#FF6347',
              '#FF4500', '#FF0000']

    color_map = branca.colormap.LinearColormap(vmin=min(circle_strengths), vmax=max(circle_strengths), colors=colors)

    for i, c in enumerate(coordinates):
        color = color_map.rgb_hex_str(x=circle_strengths[i])
        folium.Circle(location=c, radius=1000,
                      color=color,
                      fill=True, fill_color=color,
                      popup=pop_up_text[i]).add_to(vis_map)

    return vis_map


def visualize_stations(map_name: str, df: pd.DataFrame, pop_up_text_column: str, color_coding_column: str):
    tiles = 'OpenStreetMap'
    map_width = 1536
    map_height = 864

    df['color_coding'] = df[color_coding_column].factorize()[0]

    point_coordinates = [tuple(x) for x in df[[constants.LAT, constants.LON]].to_numpy()]

    center_lat = (df[constants.LAT].min() + df[constants.LAT].max()) / 2
    center_lon = (df[constants.LON].min() + df[constants.LON].max()) / 2

    vis_map = folium.Map(location=[center_lat, center_lon],
                         width=map_width, height=map_height,
                         tiles=tiles, zoom_start=7)

    vis_map = draw_circles_on_map(vis_map=vis_map,
                                  coordinates=point_coordinates,
                                  circle_strengths=df['color_coding'].tolist(),
                                  pop_up_text=df[pop_up_text_column].tolist())
    out_map_path = f'{settings.OUT_FOLDER}{map_name}.html'
    vis_map.save(outfile=out_map_path)
    print(f'Map saved to {out_map_path}')


def visualize_country_stations(country_code: str):
    df = read_ghcnd_stations(country=country_code)
    visualize_stations(map_name=f'GHCND-{country_code}', df=df)


def visualize_pjm_stations():
    map_name = f'GHCND-PJM'
    # df = read_ghcnd_stations(country='US')
    # df = df.loc[df[constants.STATE].isin(constants.PJM_STATES), :]

    df = pd.DataFrame()
    for state in constants.PJM_STATES:
        df_state = pd.read_csv(
            filepath_or_buffer=os.path.join(settings.PJM_GHCND_FOLDER, f'pjm_ghcnd_{state}.csv'),
            index_col=0
        )
        df = pd.concat([df, df_state], ignore_index=True)

    df = df.loc[df[constants.REGION].str.contains('PJM_')]

    visualize_stations(
        map_name=map_name,
        df=df,
        pop_up_text_column=constants.REGION,
        color_coding_column=constants.REGION
    )


def get_region_from_location_watt_time(latitude: float, longitude: float, token: str):
    url = "https://api.watttime.org/v3/region-from-loc"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"latitude": str(latitude), "longitude": str(longitude), "signal_type": "co2_moer"}
    response = requests.get(url, headers=headers, params=params)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise e
    response_dict = response.json()
    out = {
        'region': response_dict['region'],
        'region_full_name': response_dict['region_full_name']
    }
    return out


def get_watt_time_regions_of_ghcnd_stations(df: pd.DataFrame):
    df = df.reset_index()
    num_items = len(df)
    regions = ['NONE'] * num_items

    token, valid_until = get_watt_time_token()
    print(f'TOKEN VALID UNTIL: {valid_until} -- NOW: {datetime.datetime.now()}')

    previous_time = datetime.datetime.now()

    for idx, row in df.iterrows():

        # if datetime.datetime.now() >= valid_until:
        #    token, valid_until = get_watt_time_token()

        try:
            region_dict = get_region_from_location_watt_time(latitude=row[constants.LAT],
                                                             longitude=row[constants.LON],
                                                             token=token)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                token, valid_until = get_watt_time_token()
                print(f'TOKEN VALID UNTIL: {valid_until} -- NOW: {datetime.datetime.now()}')
                region_dict = get_region_from_location_watt_time(latitude=row[constants.LAT],
                                                                 longitude=row[constants.LON],
                                                                 token=token)
            else:
                continue

        regions[idx] = region_dict[constants.REGION]
        current_time = datetime.datetime.now()
        print(
            f'{idx+1}/{num_items}: {row[constants.ID]} {row[constants.STATE]} '
            f'({row[constants.LAT]:.4f}, {row[constants.LON]:.4f}) '
            f'--> {region_dict[constants.REGION]}, {current_time - previous_time}'
        )

        if current_time - previous_time < datetime.timedelta(milliseconds=500):
            time.sleep(0.15)

        previous_time = current_time

    df[constants.REGION] = regions
    return df


def get_pjm_regions_for_weather_stations():
    df_all = read_ghcnd_stations(country='US')

    for state in ['VA', 'WV', 'DC']:
        df = df_all.loc[df_all[constants.STATE] == state, :]
        df = get_watt_time_regions_of_ghcnd_stations(df=df)
        df.to_csv(os.path.join(settings.OUT_FOLDER, f'pjm_ghcnd_{state}.csv'))
