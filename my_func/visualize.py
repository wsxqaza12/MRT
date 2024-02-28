import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import warnings
from matplotlib.ticker import FuncFormatter
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
from . import config


custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
plt.rcParams['font.family'] = 'Microsoft JhengHei'


def plot_visitor(input_df):
    df = input_df.copy()
    
    plt.figure(figsize=(16, 5))  # Create a 1x2 grid

    # Plot the histogram on the first subplot
    plt.subplot(1, 2, 1)
    ax = sns.histplot(x='人次', data=df, bins=20, kde=True)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))  # Format x-axis labels
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))  # Format x-axis labels
    plt.title('人次的分布圖')

    # Plot the boxplot on the second subplot
    plt.subplot(1, 2, 2)
    ax = sns.boxplot(y='人次', data=df)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))  # Format y-axis labels
    plt.title('人次的Boxplot')

    # Adjust the spacing between subplots
    plt.tight_layout()
    plt.show()


def plot_station_count(df):
    plt.figure(figsize=(15, 3))
    sns.lineplot(x=df.Date, y=df.Num, linewidth=0.8)
    plt.tick_params(axis='x', labelrotation=90)
    plt.show()


def plot_station_visitor(input_df, color_map = config.color_map, color_order= config.color_order):
    df = input_df.copy()

    # Extracting the first color code from Line IDs (actual ID, not color name)
    df['Line ID'] = df['Line IDs'].apply(lambda x: x.split(',')[0])

    # Grouping the data by Line ID for plotting
    grouped_df = df.groupby('Line ID')

    # Preparing data for grouped bar plot
    bar_data = pd.concat([grouped_df.get_group(line_id) for line_id in color_order if line_id in grouped_df.groups])

    # Preparing data for grouped box plot
    box_data = pd.concat([grouped_df.get_group(line_id) for line_id in color_order if line_id in grouped_df.groups])

    # Plotting the grouped bar chart
    plt.figure(figsize=(16, 5))
    plt.gca().yaxis.set_major_formatter(
        FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    sns.barplot(x="進站", y="人次", hue="Line ID", data=bar_data, palette=color_map, dodge=False, estimator=sum)
    plt.title("進站總人次的barplot")
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel("人次")
    plt.legend(title='路線')
    plt.show()

    # Plotting the grouped boxplot
    plt.figure(figsize=(16, 5))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    sns.boxplot(x="進站", y="人次", hue="Line ID", data=box_data, palette=color_map, dodge=False, fliersize=1)
    plt.title("進站人次的boxplot")
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel("人次")
    plt.legend(title='路線')
    plt.show()


def plot_path_visitor(input_df, color_map = config.color_map, color_order= config.color_order):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        df = input_df.copy()
        fig, axes = plt.subplots(1, 2, figsize=(16, 5))

        plt.figure(figsize=(16, 5))
        sns.barplot(data=df, x='Line ID', y='人次', palette=color_map, estimator=sum, ax=axes[0], order=color_order)
        axes[0].set_title('不同線路的BarPlot')
        axes[0].set_ylabel('人次')
        axes[0].set_xlabel('線路')
        axes[0].set_xticks(range(len(color_order)))
        axes[0].set_xticklabels(color_order)
        
        # 绘制箱线图
        sns.boxplot(data=df, x='Line ID', y='人次', palette=color_map, ax=axes[1], order=color_order, fliersize=2)
        axes[1].set_title('不同線路的BoxPlot')
        axes[1].set_ylabel('人次')
        axes[1].set_xlabel('線路')
        axes[1].set_xticks(range(len(color_order)))
        axes[1].set_xticklabels(color_order)

        for ax in axes:
            ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.tight_layout()
        plt.show()


def plot_hour_visitor(input_df, by_year=False, by_station=False, station=['台北車站', '中山', '西門', '七張', '台北101/世貿']):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)

        cmap = LinearSegmentedColormap.from_list("Gradient", ["#696969", "#FFDC35", "#696969"], N=24)
        df = input_df.copy()

        if by_year:
            plt.figure(figsize=(14, 10))
            g = sns.catplot(x="時段", y="人次", data=df, palette=[cmap(i) for i in range(24)], col="year", kind="violin", inner=None)
            g.set_titles("年份: {col_name}")   
        elif by_station:
            df = df[df["進站"].isin(station)]
            g = sns.catplot(x="時段", y="人次", data=df, palette=[cmap(i) for i in range(24)], col="進站", kind="box",
                            sharey=False, legend=False, col_order=station)
            g.set_titles("車站: {col_name}")
        else:
            plt.figure(figsize=(15, 4))
            sns.boxplot(x="時段", y="人次", data=df, palette=[cmap(i) for i in range(24)], fliersize=2)
            plt.title("不同時段的人次 boxplot")
            
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
        plt.xlabel("時段")
        plt.ylabel("人次")
        plt.show()


def plot_hour_week(input_df, target):
    df = input_df.copy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning) 
        warnings.simplefilter("ignore", category=UserWarning) 

        plt.figure(figsize=(16, 5))  # Create a 1x2 grid
        df_for_box = df.groupby([target,'日期'], as_index=False)['人次'].agg(sum)
        df_for_line = df.groupby([target,'時段'], as_index=False)['人次'].agg(sum)
        week_order = ["日", "一", "二", "三", "四", "五", "六"]

        # Plot the histogram on the first subplot
        plt.subplot(1, 2, 1)
        if target == '星期':
            ax = sns.boxplot(data=df_for_box, x=target, y='人次', palette=sns.color_palette("Paired", 7), fliersize=2, order=week_order)
        else:
            ax = sns.boxplot(data=df_for_box, x=target, y='人次', palette=sns.color_palette("Paired", 7), fliersize=2)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))  # Format x-axis labels
        plt.title(f'{target}人次的boxplot')

        # Plot the boxplot on the second subplot
        plt.subplot(1, 2, 2)
        if target == '星期':
            ax = sns.lineplot(data=df_for_line, x='時段', y='人次', hue=target, hue_order=week_order, palette=sns.color_palette("Paired", 7))
        else:
            ax = sns.lineplot(data=df_for_line, x='時段', y='人次', hue=target, palette=sns.color_palette("Paired", 7))

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))  # Format y-axis labels
        x_ticks = df_for_line['時段'].unique()
        plt.xticks(ticks=x_ticks, labels=x_ticks)
        plt.title(f'{target}24小時的人次趨勢')

        # Adjust the spacing between subplots
        plt.tight_layout()
        plt.show()


def plot_line_chart_daily_all(input_df, input_abnormal=None, Mark_outliers=False, is_holiday=False, is_Typhoon=False):

    df = input_df.copy()
    df['日期'] = pd.to_datetime(df['日期'])

    # 新增一個欄位 "年份"
    df['年份'] = df['日期'].dt.year
    # 設定日期為索引
    df.set_index('日期', inplace=True)

    if Mark_outliers:
        abnormal_df = input_abnormal.copy()
        abnormal_df.set_index('日期', inplace=True)

    # 設定圖表大小
    plt.figure(figsize=(14, 8))

    # 迭代每一年，繪製每年的折線圖
    for year in df['年份'].unique():
        year_data = df[df['年份'] == year]
        sns.lineplot(x=year_data.index, y=year_data['人次'], linewidth=0.8)
        # plt.plot(year_data.index, year_data['人次'], linestyle='-', label=str(year), linewidth=0.8)

    # 在每年第一天繪製一條垂直線
    for year in df['年份'].unique():
        year_data = df[df['年份'] == year]

        # 確保有資料存在後再取得第一天的索引
        if not year_data.empty:
            first_day = year_data.index[0]
            plt.axvline(first_day, color='gray', linestyle='--', linewidth=0.8)

            # 標示文字位於虛線中點
            next_year = year + 1
            next_year_data = df[df['年份'] == next_year]

            midpoint = pd.to_datetime(f'{year}-06')

            # 在虛線中點添加標籤
            plt.text(midpoint, plt.ylim()[1], str(year), rotation=0, ha='left', va='top', color='black')

        if Mark_outliers:
            abnormal_dates = abnormal_df[abnormal_df['年份'] == year]
            # 在圖上標示出來
            if is_holiday:
                plt.scatter(abnormal_dates.index, abnormal_dates['人次'], s=8, label='Abnormal Points', c=abnormal_dates['是否放假'].map(
                    {True: '#4281A4', False: '#B0413E'})) 
                abnormal_dates_no_find = abnormal_dates[abnormal_dates['是否放假'] == False]
                
                if is_Typhoon:
                    plt.scatter(abnormal_dates.index, abnormal_dates['人次'], s=8, label='Typhoon', c=abnormal_dates['是否停止上班上課'].map(
                        {True: '#D3A0DB', False: 'none'}))
                    # 輸出異常日期
                    abnormal_dates_no_find = abnormal_dates[(abnormal_dates['是否放假'] == False) & (abnormal_dates['是否停止上班上課'] == False)]

                if not abnormal_dates_no_find.empty:
                    print(f"Year {year} - Abnormal Dates: {abnormal_dates_no_find.index.tolist()}")

            else:
                plt.scatter(abnormal_dates.index,
                            abnormal_dates['人次'], s=8, color='#B0413E', label='Abnormal Points')               
                if not abnormal_dates.empty:
                    print(f"Year {year} - Abnormal Dates: {abnormal_dates.index.tolist()}")

    # 格式化 y 軸標籤為不使用科學記號
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    plt.xlabel('')
    plt.ylabel('人次')
    plt.show()


def plot_abnormal_isholiday(input_df, columns_to_plot=['星期', '是否放假', '備註']):
    df = input_df.copy()
    # 設定畫布大小
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # 使用 for 迴圈繪製 countplot
    for i, column in enumerate(columns_to_plot):
        sns.countplot(x=column, data=df, hue='年份', ax=axes[i])
        axes[i].set_title(f'{column}', fontsize=16)
        axes[i].set_xlabel('', fontsize=14)
        axes[i].set_ylabel('Count', fontsize=14)

    # 調整子圖之間的間距
    plt.tight_layout()
    plt.tick_params(axis='x', labelrotation=90)
    # 顯示圖形
    plt.show()


def plot_line_chart_daily_covid(input_df, covid_target):
    # 複製 DataFrame 以防修改原始資料
    df = input_df.copy()
    df['日期'] = pd.to_datetime(df['日期'])

    # 新增一個欄位 "年份"
    df['年份'] = df['日期'].dt.year
    # 設定日期為索引
    df.set_index('日期', inplace=True)

    # 設定圖表大小
    plt.figure(figsize=(14, 8))

    # 創建一個主要的 axes
    ax1 = plt.gca()

    # 迭代每一年，繪製每年的折線圖
    for year in df['年份'].unique():
        year_data = df[df['年份'] == year]
    
        # 第一個 sns.lineplot，將 y 軸設置為左邊
        sns.lineplot(x=year_data.index, y=year_data['人次'], linewidth=0.8, ax=ax1)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    
    # 創建第二個 y 軸
    ax2 = ax1.twinx()

    # 再次迭代每一年，繪製第二條折線圖，將 y 軸設置為右邊，顏色設置為黑色
    for year in df['年份'].unique():
        year_data = df[df['年份'] == year]
        sns.lineplot(x=year_data.index, y=year_data[covid_target], linewidth=0.8, ax=ax2, color='black')

    # 在每年第一天繪製一條垂直線
    for year in df['年份'].unique():
        year_data = df[df['年份'] == year]

        # 確保有資料存在後再取得第一天的索引
        if not year_data.empty:
            first_day = year_data.index[0]
            plt.axvline(first_day, color='gray', linestyle='--', linewidth=0.8)

            # 標示文字位於虛線中點
            next_year = year + 1
            next_year_data = df[df['年份'] == next_year]

            midpoint = pd.to_datetime(f'{year}-06')

            # 在虛線中點添加標籤
            plt.text(midpoint, plt.ylim()[1], str(year), rotation=0, ha='left', va='top', color='black')

    # 可以自行調整標籤、標題等等
    # 格式化 y 軸標籤為不使用科學記號
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    ax1.set_xlabel('日期')
    ax1.set_ylabel('人次', color='black')
    ax2.set_ylabel(covid_target, color='black')

    plt.show()


def plot_boxplot_monthly(input_df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning) 
        warnings.simplefilter("ignore", category=UserWarning)
        
        df = input_df.copy()

        df['年月'] = df['日期'].dt.to_period('M')  # 建立年月欄位
        df['年'] = df['日期'].dt.year  # 建立年份欄位

        numeric_columns = ['人次']

        # 以年月和進站分組，準備畫 boxplot
        plt.figure(figsize=(14, 8))

        # 設定漸層色
        colors = ['#70B443', '#DE6059', '#D79A5A', '#5B8AC3']
        cmap = LinearSegmentedColormap.from_list('custom', colors, N=12)

        # 取得所有年份的唯一值
        unique_years = df['年'].unique()

        max_height = 0  # 初始化最大高度
        for i, year in enumerate(unique_years):
            # 根據年份篩選資料
            df_year = df[df['年'] == year]
            
            # 在每年1月添加垂直線
            plt.axvline(x=f'{year}-01', color='gray', linestyle='--', linewidth=1)
            
            # 計算漸層色的索引
            gradient_indices = [i % 12 for i in range(12)]
            
            # 畫 boxplot，使用漸層色
            sns.boxplot(x='年月', y=numeric_columns[0], data=df_year, palette=[cmap(idx) for idx in gradient_indices], width=0.7, fliersize=2)

            # 計算最大高度，for text
            max_height = max(max_height, df_year[numeric_columns[0]].max() + 60)

        # 在虛線上方標註該年份，水平擺放 text
        for i, year in enumerate(unique_years):
            plt.text(f'{year}-06', max_height, str(year), rotation=0, ha='left', va='bottom', color='black')

        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
        plt.xticks(rotation=90)  # 調整 x 軸刻度標籤的角度
        plt.show()

def plot_quarter_visitor(input_df, color_map = config.color_map):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        warnings.simplefilter("ignore", category=UserWarning)
        df = input_df.copy()
        custom_labels = ['春季', '夏季', '秋季', '冬季']
        fig, axes = plt.subplots(1, 2, figsize=(16, 5))

        plt.figure(figsize=(16, 5))
        sns.barplot(data=df, x='quarter', y='人次', palette=color_map, estimator=sum, ax=axes[0])
        axes[0].set_title('不同季節的BarPlot')
        axes[0].set_ylabel('人次')
        axes[0].set_xlabel('季節')
        axes[0].set_xticklabels(custom_labels)
        
        # 绘制箱线图
        sns.boxplot(data=df, x='quarter', y='人次', palette=color_map, ax=axes[1], fliersize=2)
        axes[1].set_title('不同季節的BoxPlot')
        axes[1].set_ylabel('人次')
        axes[1].set_xlabel('季節')
        axes[1].set_xticklabels(custom_labels)


        for ax in axes:
            ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.tight_layout()
        plt.show()


def plot_weather_scatter(input_df, target=None):
    df = input_df.copy()

    plt.figure(figsize=(16, 5))  # Create a 1x2 grid
    # Plot the histogram on the first subplot
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=df, x='temperature', y='人次', alpha=0.3, edgecolor='none', hue=target)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    plt.xlabel('溫度 (°C)')

    # 繪製 人次 vs 雨量
    plt.subplot(1, 2, 2)
    sns.scatterplot(data=df, x='rainfall', y='人次', alpha=0.3, edgecolor='none', hue=target)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    plt.xlabel('雨量 (mm)')
    # Adjust the spacing between subplots

    plt.tight_layout()
    plt.show()


def plot_weather_box(input_df, color_map=config.color_map):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        warnings.simplefilter("ignore", category=UserWarning)
        df = input_df.copy()

        plt.figure(figsize=(16, 5))  # 設定圖形大小

        plt.subplot(1, 2, 1)
        temperature_order = ["<10", "10~20", "20~30", ">30"]
        sns.boxplot(data=df, x='temperature_level', y='人次', fliersize=2, palette=color_map, order=temperature_order)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
        plt.xlabel('溫度級別')


        plt.subplot(1, 2, 2)
        sns.set(style="whitegrid")

        existing_rainfall_levels = df['rainfall_level'].unique()
        rainfall_order = ["無雨", "小雨", "中雨", "大雨", "豪雨", "大豪雨", "超大豪雨"]
        rainfall_order = [level for level in rainfall_order if level in existing_rainfall_levels]

        sns.boxplot(data=df, x='rainfall_level', y='人次', fliersize=2, palette='Blues_d', order=rainfall_order)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
        plt.xlabel('降雨級別')

        # 顯示圖形
        plt.show()

def plot_model_real_predict(result):
    plt.figure(figsize=(14, 3))
    result = result.sort_values(by='日期')
    
    # 使用Seaborn繪製折線圖
    sns.lineplot(x='日期', y='y', data=result, label='實際人次')
    sns.lineplot(x='日期', y='y_predict', data=result, label='預測人次')

    # 添加標籤和標題
    plt.xlabel('日期')
    plt.ylabel('人次')
    plt.title('y vs. y_predict 每日人次')


    # 旋轉日期標籤以避免重疊
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    plt.show()