import pandas as pd
import folium
from . import config


def MRT_location_mean(csv_path):
    df_stations = pd.read_csv(csv_path, encoding='Big5')

    # Split the '出入口名稱' and keep the station name
    df_stations['捷運站名稱'] = df_stations['出入口名稱'].str.split('站').str[0]
    # df_stations['捷運站名稱'] = df_stations['捷運站名稱'].str.replace('站', '')
    df_stations['捷運站名稱'] = df_stations['捷運站名稱'].str.replace('台北車', '台北車站')

    # Group by the new station name column and calculate the mean of the coordinates
    df_avg_station_coords = df_stations.groupby('捷運站名稱').agg({
        '緯度': 'mean',
        '經度': 'mean'
    }).reset_index()

    return df_avg_station_coords


def process_and_merge_MRT_info(location_path, path_Taipei, path_NewTaipei):
    df_avg_station_coords = MRT_location_mean(location_path)

    station_Taipei = pd.read_csv(path_Taipei)
    station_NewTaipei = pd.read_csv(path_NewTaipei)
    df_station_colors = pd.concat([station_Taipei, station_NewTaipei], ignore_index=True)

    # Merge the average coordinates DataFrame with the station colors DataFrame on the modified '捷運站名稱' and 'Zh_tw'
    df_avg_station_coords_colors = df_avg_station_coords.merge(df_station_colors, left_on='捷運站名稱', right_on='Station Name (Zh-TW)', how='left')

    # Sort the data by LineID and Sequence
    df_sorted = df_avg_station_coords_colors.sort_values(['Route Name (Zh-TW)', 'Sequence'])

    return df_sorted


# def create_circle_and_path_map(df, lat_col='緯度', lon_col='經度', name_col='捷運站名稱', line_id_col='Route ID', color_map=config.color_map):
#     map_center = [df[lat_col].median(), df[lon_col].median()]
#     map = folium.Map(location=map_center, zoom_start=12,tiles='CartoDB dark_matter', attr='Map tiles by Stamen Design under ODbL')


#     for line_id in df[line_id_col].unique():
#         # Extract the coordinates for each line
#         line_data = df[df[line_id_col] == line_id]
#         line_coords = line_data[['緯度', '經度']].values.tolist()
#         index_of_Line_id = line_data['Line ID'].index[0]
#         color = line_data['Line ID'][index_of_Line_id]

#         # Plot the line on the map
#         folium.PolyLine(
#             line_coords,
#             color=color_map.get(color, 'gray'),  # Use the color mapping, default to gray if not found
#             weight=3.5,
#             opacity=0.7
#         ).add_to(map)
        
#     for idx, row in df.iterrows():
#         color = color_map.get(row['Line ID'], 'gray')

#         # Add a solid circular marker to the map
#         folium.Circle(
#             location=[row[lat_col], row[lon_col]],
#             radius=100,  # Fixed radius for all markers
#             color=color,
#             fill=True,
#             fill_color=color,
#             fill_opacity=0.7,
#             popup=row[name_col]
#         ).add_to(map)

#         # Add station name as a label
#         # folium.Marker(
#         #     location=[row[lat_col], row[lon_col]],
#         #     icon=folium.DivIcon(html=f'<div style="font-size: 10pt">{row[name_col]}</div>')
#         # ).add_to(map)

#     folium.LayerControl().add_to(map)
#     return map