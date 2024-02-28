import pandas as pd
import folium
from . import config


def plot_map(MRT_info=None, stations_info=None):
    if stations_info is not None:
        map_center = stations_info['Latitude'].median(), stations_info['Longitude'].median()
    elif MRT_info is not None:
        map_center = [MRT_info['緯度'].median(), MRT_info['經度'].median()]

    map = folium.Map(location=map_center, zoom_start=12,tiles='CartoDB dark_matter', attr='Map tiles by Stamen Design under ODbL')

    if stations_info is not None:
        map = create_colored_marker_map(map, stations_info)
    if MRT_info is not None:
        map = create_circle_and_path_map(map, MRT_info)
    
    return map


def create_circle_and_path_map(m, df, lat_col='緯度', lon_col='經度', name_col='捷運站名稱', line_id_col='Route ID', color_map=config.color_map):
    map_center = [df[lat_col].median(), df[lon_col].median()]
    # map = folium.Map(location=map_center, zoom_start=12,tiles='CartoDB dark_matter', attr='Map tiles by Stamen Design under ODbL')


    for line_id in df[line_id_col].unique():
        # Extract the coordinates for each line
        line_data = df[df[line_id_col] == line_id]
        line_coords = line_data[['緯度', '經度']].values.tolist()
        index_of_Line_id = line_data['Line ID'].index[0]
        color = line_data['Line ID'][index_of_Line_id]

        # Plot the line on the map
        folium.PolyLine(
            line_coords,
            color=color_map.get(color, 'gray'),  # Use the color mapping, default to gray if not found
            weight=3.5,
            opacity=0.7
        ).add_to(m)
        
    for idx, row in df.iterrows():
        color = color_map.get(row['Line ID'], 'gray')

        # Add a solid circular marker to the map
        folium.Circle(
            location=[row[lat_col], row[lon_col]],
            radius=100,  # Fixed radius for all markers
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=row[name_col]
        ).add_to(m)

        # Add station name as a label
        # folium.Marker(
        #     location=[row[lat_col], row[lon_col]],
        #     icon=folium.DivIcon(html=f'<div style="font-size: 10pt">{row[name_col]}</div>')
        # ).add_to(map)

    folium.LayerControl().add_to(m)
    return m


def create_colored_marker_map(m, data, latitude_col='Latitude', longitude_col='Longitude', group_col='City', group_colors=config.color_map):
    # 创建地图对象

    # 获取数据中的不同组
    groups = data[group_col].unique()

    for group in groups:
        group_data = data[data[group_col] == group]
        feature_group = folium.FeatureGroup(name=f'Group {group}')

        for _, row in group_data.iterrows():
            folium.CircleMarker(
                location=[row[latitude_col], row[longitude_col]],
                radius=5,
                popup=f"StID: {row['StID']}",
                color=group_colors.get(group, 'gray'),  # 使用默认颜色'gray'，如果组不在group_colors字典中
                fill=True,
                fill_color=group_colors.get(group, 'gray'),  # 同样使用默认颜色
                fill_opacity=0.7
            ).add_to(feature_group)

        feature_group.add_to(m)

    # 添加图例
    folium.LayerControl().add_to(m)
    
    return m

# def create_colored_marker_map(data, latitude_col='Latitude', longitude_col='Longitude', group_col='City', group_colors=config.color_map):
#     # 创建地图对象
#     m = folium.Map(location=[data[latitude_col].mean(), data[longitude_col].mean()], zoom_start=12, tiles='CartoDB dark_matter', attr='Map tiles by Stamen Design under ODbL')

#     # 获取数据中的不同组
#     groups = data[group_col].unique()

#     for group in groups:
#         group_data = data[data[group_col] == group]
#         feature_group = folium.FeatureGroup(name=f'Group {group}')

#         for _, row in group_data.iterrows():
#             folium.CircleMarker(
#                 location=[row[latitude_col], row[longitude_col]],
#                 radius=5,
#                 popup=f"StID: {row['StID']}",
#                 color=group_colors.get(group, 'gray'),  # 使用默认颜色'gray'，如果组不在group_colors字典中
#                 fill=True,
#                 fill_color=group_colors.get(group, 'gray'),  # 同样使用默认颜色
#                 fill_opacity=0.7
#             ).add_to(feature_group)

#         feature_group.add_to(m)

#     # 添加图例
#     folium.LayerControl().add_to(m)
    
#     return m