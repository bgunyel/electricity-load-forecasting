import branca
import folium
import pandas as pd

from config import settings, constants
from source.data_utils import read_ghcnd_stations


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


def visualize_stations(map_name: str, df: pd.DataFrame):
    tiles = 'OpenStreetMap'
    map_width = 1536
    map_height = 864

    df[constants.STATE_ID] = df[constants.STATE].factorize()[0]

    point_coordinates = [tuple(x) for x in df[[constants.LAT, constants.LON]].to_numpy()]

    center_lat = (df[constants.LAT].min() + df[constants.LAT].max()) / 2
    center_lon = (df[constants.LON].min() + df[constants.LON].max()) / 2

    vis_map = folium.Map(location=[center_lat, center_lon],
                         width=map_width, height=map_height,
                         tiles=tiles, zoom_start=7)

    vis_map = draw_circles_on_map(vis_map=vis_map,
                                  coordinates=point_coordinates,
                                  circle_strengths=df[constants.STATE_ID].tolist(),
                                  pop_up_text=df[constants.ID].tolist())
    out_map_path = f'{settings.OUT_FOLDER}{map_name}.html'
    vis_map.save(outfile=out_map_path)
    print(f'Map saved to {out_map_path}')


def visualize_country_stations(country_code: str):
    df = read_ghcnd_stations(country=country_code)
    visualize_stations(map_name=f'GHCND-{country_code}', df=df)


def visualize_pjm_stations():
    map_name = f'GHCND-PJM'
    df = read_ghcnd_stations(country='US', )
    df = df.loc[df[constants.STATE].isin(constants.PJM_STATES), :]
    visualize_stations(map_name=map_name, df=df)
