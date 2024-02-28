import pandas as pd
import requests


def download_files_from_csv(csv_file_path, destination_folder, start=0):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = pd.read_csv(csvfile)

        for i in range(start, len(reader)):
            # 取得URL
            url = reader.URL[i]

            # 產生保存檔案的路徑和檔案名
            file_name = f"file_{reader.年月[i]}.csv"  # 使用 '年月' 作為 欄位名稱
            destination_file = destination_folder + file_name

            response = requests.get(url)
            if response.status_code == 200:
                with open(destination_file, 'wb') as file:
                    file.write(response.content)
                print(f"文件 {file_name} 下載成功！")
            else:
                print(f"文件 {file_name} 下載成功。HTTP狀態:", response.status_code)
