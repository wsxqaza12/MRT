from pandas.api.types import is_numeric_dtype
from sklearn.metrics import mean_absolute_percentage_error
import catboost as cb
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def split_X_y_by_time(df, test_start, test_end,
                      date_col='日期', y_col=['人次']):
    """
    Divide the dataframe into train and test for X and Y respectively
    """
    date_ar = df[date_col]
    X, y = split_X_y(df, date_col, y_col)

    train_row = date_ar <= test_start
    test_row = (date_ar > test_start) & (date_ar <= test_end)
    X_train, X_test = X[train_row], X[test_row]
    y_train, y_test = y[train_row], y[test_row]

    return X_train, X_test, y_train, y_test


def split_backtest(df, time=3, day=9, date_col='date'):
    """
    Get the time of each interval of Backtesting
    """

    time_end = df[date_col].unique().max()
    time_end = pd.to_datetime(time_end, format='%Y-%m-%d')
    test_start = []
    test_end = []

    for i in range(time):
        split_date = time_end - datetime.timedelta(days=day)
        test_start.append(split_date)
        test_end.append(time_end)
        time_end = split_date

    test_time_range = [test_start, test_end]
    return test_time_range


def split_X_y(df, date_col, y_col):
    """
    Divide the dataframe into two: X and Y
    """
    x_col = list(set(df) - set(y_col) - set([date_col]))

    y = df[y_col]
    X = df[x_col]

    return X, y


def get_categorical_indicies(df):
    """
    Indicate category columns
    """

    cats = []
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            pass
        else:
            cats.append(col)
    cat_indicies = []
    for col in cats:
        cat_indicies.append(df.columns.get_loc(col))
    return cat_indicies


def backtest_predict(backtesting_times, data_dropna):
    record = []
    for k in range(backtesting_times):
        test_start = test_time_range[0][k]
        test_end = test_time_range[1][k]

        X_train, X_test, y_train, y_test = split_X_y_by_time(
            data_dropna, test_start, test_end)
        categorical_indicies = get_categorical_indicies(X_train)

        train_dataset = cb.Pool(
            X_train, y_train, cat_features=categorical_indicies)
        test_dataset = cb.Pool(
            X_test, y_test, cat_features=categorical_indicies)

        model = cb.CatBoostRegressor(iterations=3000,
                                        task_type="GPU")

        model.fit(train_dataset)
        y_predict = model.predict(test_dataset)
        MAPE_vaule = mean_absolute_percentage_error(y_true=y_test['人次'], y_pred=y_predict)

        record.append({
            '日期': test_end,
            'y': y_test['人次'].sum(),
            'y_predict': y_predict.sum(),
            'MAPE': MAPE_vaule,
        })

    record_data = pd.DataFrame(interpolated_data_list)
    return record_data


def plot_feature_importance(importance, names, model_type):
    """
    plot feature importance
    """

    # Create arrays from feature importance and feature names
    feature_importance = np.array(importance)
    feature_names = np.array(names)

    # Create a DataFrame using a Dictionary
    data = {'feature_names': feature_names,
            'feature_importance': feature_importance}
    fi_df = pd.DataFrame(data)

    # Sort the DataFrame in order decreasing feature importance
    fi_df.sort_values(by=['feature_importance'], ascending=False, inplace=True)

    # Define size of bar plot
    fig = plt.figure(figsize=(10, 8))
    # Plot Searborn bar chart
    sns.barplot(x=fi_df['feature_importance'], y=fi_df['feature_names'])
    # Add chart labels
    plt.title(model_type + ' FEATURE IMPORTANCE')
    plt.xlabel('FEATURE IMPORTANCE')
    plt.ylabel('FEATURE NAMES')

    return fig