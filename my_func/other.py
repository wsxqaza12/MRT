import os
import glob
import pandas as pd

def count_station_number_by_yearmo(path):

    extension = 'csv'
    os.chdir(path)
    file_paths = glob.glob('*.{}'.format(extension))

    stations = pd.DataFrame(columns=['Date', 'Num'])
    all_data = pd.DataFrame()

    # 逐一載入並合併
    for file in file_paths: 
        data = pd.read_csv(file)
        year = file[5:9]
        month = file[9:11]
        # 進行進站獨特數量的計算
        unique_stations = data['進站'].nunique()

        # 使用 loc 方法添加新行
        stations.loc[len(stations)] = {'Date': year+month, 'Num': unique_stations}

    return stations


def find_outlier(input_df):
    df = input_df.copy()

    # 將"日期"欄位轉換成日期格式
    df['日期'] = pd.to_datetime(df['日期'])
    # 新增一個欄位 "年份"
    df['年份'] = df['日期'].dt.year
    # 設定日期為索引
    df.set_index('日期', inplace=True)

    abnormal_df = pd.DataFrame()

    # 在每年第一天繪製一條垂直線
    for year in df['年份'].unique():
        year_data = df[df['年份'] == year]

        mean_value = year_data['人次'].mean()
        std_value = year_data['人次'].std()
        upper_threshold, lower_threshold = mean_value + 1.96 * std_value, mean_value - 1.96 * std_value

        abnormal_dates = year_data[(year_data['人次'] > upper_threshold) | (year_data['人次'] < lower_threshold)].reset_index()
        abnormal_df = pd.concat([abnormal_df, abnormal_dates], ignore_index=True)

    return abnormal_df


# 定義一個函數來計算溫度級別
def temperature_level(temperature):
    if temperature < 10:
        return "<10"
    elif 10 <= temperature < 20:
        return "10~20"
    elif 20 <= temperature < 30:
        return "20~30"
    else:
        return ">30"

# 定義一個函數來計算降雨級別
def rainfall_level(rainfall):
    if rainfall == 0:
        return "無雨"
    elif 0 < rainfall <= 10:
        return "小雨"
    elif 10 < rainfall <= 80:
        return "中雨"
    elif 80 < rainfall <= 239:
        return "大雨"
    elif 239 < rainfall <= 349:
        return "豪雨"
    elif 349 < rainfall <= 500:
        return "大豪雨"
    else:
        return "超大豪雨"