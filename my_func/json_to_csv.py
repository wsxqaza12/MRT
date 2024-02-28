import json
import csv
import pandas as pd

def convert_json_to_csv(json_file_path, csv_file_path):
    # 讀取 Json
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 取得 header 與 rows
    header = ["LineNo", "LineID", "Sequence", "StationID", "Zh_tw", "En"]
    rows = []

    for item in data:
        line_no = item["LineNo"]
        line_id = item["LineID"]

        for station in item["Stations"]:
            sequence = station["Sequence"]
            station_id = station["StationID"]
            zh_tw = station["StationName"]["Zh_tw"]
            en = station["StationName"]["En"]

            rows.append([line_no, line_id, sequence, station_id, zh_tw, en])

    # 寫成 CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"CSV file '{csv_file_path}' has been created.")


def convert_path_json_to_csv(json_file_path, csv_file_path):
    # Load the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Flatten the 'Stations' field and handle missing fields with errors='ignore'
    df_stations = pd.json_normalize(
        data, 
        record_path=['Stations'], 
        meta=[
            'LineNo', 
            'LineID', 
            'RouteID', 
            'Direction', 
            'SrcUpdateTime', 
            'UpdateTime', 
            'VersionID', 
            ['RouteName', 'Zh_tw'], 
            ['RouteName', 'En']
        ],
        errors='ignore'
    )

    # Rename columns for clarity
    df_stations.rename(columns={
        'StationID': 'Station ID',
        'StationName.Zh_tw': 'Station Name (Zh-TW)',
        'StationName.En': 'Station Name (En)',
        'LineNo': 'Line Number',
        'LineID': 'Line ID',
        'RouteID': 'Route ID',
        'Direction': 'Direction',
        'SrcUpdateTime': 'Source Update Time',
        'UpdateTime': 'Update Time',
        'VersionID': 'Version ID',
        'RouteName.Zh_tw': 'Route Name (Zh-TW)',
        'RouteName.En': 'Route Name (En)'
    }, inplace=True)

    # Save the DataFrame to a CSV file
    df_stations.to_csv(csv_file_path, index=False)

    # Return a message indicating success
    return f"CSV file saved at: {csv_file_path}"

