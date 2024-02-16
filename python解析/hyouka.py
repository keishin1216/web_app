import numpy as np
from sklearn.metrics import mean_squared_error
from scipy.spatial.distance import euclidean
from sklearn.metrics import mutual_info_score
import pandas as pd
import math
from scipy.stats import pearsonr

# CSVファイルからデータを読み込む
df1 = pd.read_csv('../plus_data.csv/むらさき2 鈴木.csv')
df2 = pd.read_csv('../eda改/2周目 eda 鈴木.csv')

# 関数 f の定義
def f(a, b, x):
    return (a * np.exp(-(((x / 3) - (b / 3))**2 / 2))) / (math.sqrt(2 * math.pi))

# 関数 g の定義
def g(x, a_values, b_values):
    result = np.zeros_like(x, dtype=np.float64)
    for a, b in zip(a_values, b_values):
        result += f(a, b, x)
    return result

N = 5000
xmin = 0
xmax = 140
ymin, ymax = -5, 15
x_spot = 0
p = np.linspace(xmin, xmax, N)

curve1 = g(p, df1['buttonNumber'].values, df1['time(min)'].values)
curve2 = g(p, df2['buttonNumber'].values, df2['time(min)'].values)
normalized_curve1 = (curve1 - np.min(curve1)) / (np.max(curve1) - np.min(curve1))
normalized_curve2 = (curve2 - np.min(curve2)) / (np.max(curve2) - np.min(curve2))



# 相関係数と p 値を計算
correlation_coefficient, p_value = pearsonr(normalized_curve1, normalized_curve2)
correlation_coefficient, _ = pearsonr(normalized_curve1, normalized_curve2)
print(f"相関係数: {correlation_coefficient}")

# p 値の表示
print(f"P 値: {p_value}")


# 平均二乗誤差 (MSE) の計算
mse = mean_squared_error(normalized_curve1, normalized_curve2)
print(f"Mean Squared Error: {mse}")

# ユークリッド距離の計算
euclidean_distance = euclidean(normalized_curve1, normalized_curve2)
print(f"Euclidean Distance: {euclidean_distance}")

# 相互情報量 (Mutual Information) の計算
# 注意: 相互情報量を計算するにはデータが離散的である必要があります
data1_discrete = np.digitize(normalized_curve1, bins=np.arange(min(normalized_curve1), max(normalized_curve1), 1))
data2_discrete = np.digitize(normalized_curve2, bins=np.arange(min(normalized_curve2), max(normalized_curve2), 1))

mutual_info = mutual_info_score(data1_discrete, data2_discrete)
print(f"Mutual Information: {mutual_info}")
