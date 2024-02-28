import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

class AnovaAnalyzer:
    def __init__(self, df, value_column, group_column, alpha=0.05):
        self.df = df
        self.value_column = value_column
        self.group_column = group_column
        self.alpha = alpha
        self.result = None
        self.f_statistic = None
        self.p_value = None
        self.posthoc_results = None

    def perform_anova(self):
        groups = [self.df[self.df[self.group_column] == group][self.value_column]
                  for group in self.df[self.group_column].unique()]

        # 執行一元變異數分析
        self.f_statistic, self.p_value = f_oneway(*groups)

        # 判斷結果
        if self.p_value < self.alpha:
            self.result = "統計上有顯著差異，我們拒絕虛無假設"
        else:
            self.result = "統計上沒有顯著差異，我們無法拒絕虛無假設"

        return self.f_statistic, self.p_value, self.result

    def display_result(self):
        print(f'F-statistic: {self.f_statistic}')
        print(f'P-value: {self.p_value}')
        print(self.result)

    def perform_posthoc(self):
        # Perform Tukey-Kramer post-hoc test
        posthoc = pairwise_tukeyhsd(self.df[self.value_column], self.df[self.group_column])
        self.posthoc_results = posthoc

    def display_posthoc(self):
        if self.posthoc_results is not None:
            print("事後檢定結果:")
            print(self.posthoc_results)
        else:
            print("尚未執行事後檢定。請呼叫 perform_posthoc() 進行執行。")
