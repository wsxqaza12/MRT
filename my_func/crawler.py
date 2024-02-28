import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re


def crawler_Typhoon_info_to_csv(url, destination_folder, file_name):
    try:
        # 發送GET請求，並取得網頁內容
        response = requests.get(url)
        response.raise_for_status()  # 如果請求失敗，拋出異常

        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到表格的HTML標籤
        table = soup.find('table')

        # 將HTML字串包裝成StringIO物件，再使用pandas的read_html函數將HTML表格轉換為DataFrame
        df = pd.read_html(StringIO(str(table)))[0]

        file_path = f"{destination_folder + file_name}.csv"
        # 將DataFrame儲存為CSV檔案
        df.to_csv(file_path, index=False, encoding='utf-8-sig')

        print(f"CSV檔案已建立：{file_name}")
    except requests.exceptions.RequestException as e:
        print(f"發生錯誤：{e}")


def scrape_date_Stop_work(input_df):
    df = input_df.copy()

    # 新增兩個欄位：停止日期和是否停止上班上課
    df['停止日期'] = df['臺北市停止上班上課情形'].apply(lambda x: re.search(r'\d+月\d+日', x).group() if re.search(r'\d+月\d+日', x) else '')
    df['停止日期'] = df.apply(lambda row: f"{row['年']+1911}年{row['停止日期']}", axis=1)
    df[['停止日期']] = df[['停止日期']].apply(date_manipulate)

    df['是否停止上班上課'] = df['臺北市停止上班上課情形'].apply(lambda x: False if '照常' in x or '未達' in x else True)
    df['停止日期'] = pd.to_datetime(df['停止日期'], format='%Y-%m-%d')

    selected_columns = df[['天然災害名稱', '停止日期', '是否停止上班上課']].copy()

    return selected_columns


def date_manipulate(x):
    x = x.str.split('日').str[0].add('日')
    x = x.str.replace('年', '-').str.replace('月', '-').str.replace('日', '')
    x = pd.to_datetime(x, format='%Y-%m-%d', errors='coerce').dt.date
    
    return x