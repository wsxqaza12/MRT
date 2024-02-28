import os
import glob
import pandas as pd


def merged_to_daily(path, group, destination_folder, file_name):

    extension = 'csv'
    os.chdir(path)
    file_paths = glob.glob('*.{}'.format(extension))

    merged_df = pd.DataFrame()

    # 讀取每個CSV檔案並合併數據
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        daily_sum = df.groupby(group, as_index=False)['人次'].agg('sum')
        merged_df = pd.concat([merged_df, daily_sum], ignore_index=True)

    merged_revise = merged_df.groupby(group, as_index=False)['人次'].agg('sum')

    file_path = f"{destination_folder + file_name}"
    merged_revise.to_csv(file_path, index=False)


def map_to_general_station_name(station_name):
    # Ensure the station name is a string before checking its content
    if isinstance(station_name, str) and '板橋' in station_name:
        return '板橋'
    
    return station_name

def merged_MRT_info_with_ori_data(input_df, input_MRT_info):
    df = input_df.copy()
    MRT_info = input_MRT_info.copy()
    rest_MRT_info = MRT_info[['捷運站名稱', 'Line ID']].drop_duplicates()

    # Replacing missing or non-string values in 'Line ID' with an empty string
    rest_MRT_info['Line ID'] = rest_MRT_info['Line ID'].apply(lambda x: x if isinstance(x, str) else '')
    rest_MRT_info['捷運站名稱'] = rest_MRT_info['捷運站名稱'].str.replace('大橋頭', '大橋頭站')
    grouped_rest_MRT_info = rest_MRT_info.groupby('捷運站名稱')['Line ID'].apply(lambda x: ','.join(filter(None, x))).reset_index()
    grouped_rest_MRT_info.rename(columns={'Line ID': 'Line IDs'}, inplace=True)

    # Apply the updated function to create the new 'GeneralStationName' column
    df['GeneralStationName'] = df['進站'].apply(map_to_general_station_name)
    joined_df = pd.merge(df, grouped_rest_MRT_info, how='inner', left_on='GeneralStationName', right_on='捷運站名稱')
    joined_df.loc[joined_df['進站'] == 'BL板橋', 'Line IDs'] = 'BL'
    joined_df.loc[joined_df['進站'] == 'Y板橋', 'Line IDs'] = 'Y'

    columns_to_drop = ['GeneralStationName', '捷運站名稱']
    joined_df.drop(columns=columns_to_drop, inplace=True)

    return joined_df


def merged_holiday(path, destination_folder, file_name):

    extension = 'csv'
    os.chdir(path)
    file_paths = glob.glob('*.{}'.format(extension))

    merged_df = pd.DataFrame()

    # 讀取每個CSV檔案並合併數據
    for file_path in file_paths:
        df = pd.read_csv(file_path, encoding='Big5')
        merged_df = pd.concat([merged_df, df], ignore_index=True)

    merged_df['是否放假'] = merged_df['是否放假'].replace(2, 1)
    merged_df['是否放假'] = merged_df['是否放假'].astype(bool)
    merged_df['備註'].fillna('無特別', inplace=True)

    file_path = f"{destination_folder + file_name}.csv"
    merged_df.to_csv(file_path, index=False)


def merged_abnormal_typhoon(abnormal, Typhoon):
    abnormal_holiday_Typhoon = pd.merge(abnormal, Typhoon, left_on='日期', right_on='停止日期', how='left')
    abnormal_holiday_Typhoon['天然災害名稱'].fillna('無', inplace=True)
    abnormal_holiday_Typhoon['是否停止上班上課'].fillna(False, inplace=True)

    columns_to_drop = ['西元日期', '停止日期']
    abnormal_holiday_Typhoon = abnormal_holiday_Typhoon.drop(columns=columns_to_drop)

    return abnormal_holiday_Typhoon

def merged_Meteorology_to_ori_data(input_df, input_Meteorology):
    df = input_df.copy()
    Meteorology = input_Meteorology

    # Replacing missing or non-string values in 'Line ID' with an empty string
    Meteorology['捷運站名稱'] = Meteorology['捷運站名稱'].str.replace('大橋頭', '大橋頭站')

    # Apply the updated function to create the new 'GeneralStationName' column
    df['GeneralStationName'] = df['進站'].apply(map_to_general_station_name)
    joined_df = pd.merge(df, Meteorology, how='inner', left_on=['日期','GeneralStationName'], right_on=['Date','捷運站名稱'])

    columns_to_drop = ['GeneralStationName', '捷運站名稱']
    joined_df.drop(columns=columns_to_drop, inplace=True)

    return joined_df
