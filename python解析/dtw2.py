from fastdtw import fastdtw
from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# CSVファイルからデータを読み込む
df1 = pd.read_csv('../plus_data.csv/浜.csv')
df2 = pd.read_csv('../eda改/1周目 eda はま.csv')
# 関数 f の定義
def f(a, b, x):
    c = i
    return (a * np.exp(-(((x / c) - (b / c))**2 / 2))) / (math.sqrt(2 * math.pi))
i = float(input("パラメータ:"))
# 関数 g の定義
def g(x, a_values, b_values):
    result = np.zeros_like(x, dtype=np.float64)
    for a, b in zip(a_values, b_values):
        result += f(a, b, x)
    return result




# 曲線をプロット
N = 5000
xmin = 0
xmax = 120
ymin, ymax = -5, 15
x_spot = 0
p = np.linspace(xmin, xmax, N)
curve1 = g(p, df1['buttonNumber'].values, df1['time(min)'].values)
curve2 = g(p, df2['buttonNumber'].values, df2['time(min)'].values)

#plt.plot(p, curve1)
#plt.plot(p, curve2)


plt.ylim(ymin, ymax)
#plt.legend()
#plt.show()
# 既存のプロットコード

time_values_original = df1['time(min)'].values


# curve1 と curve2 を正規化
normalized_curve1 = (curve1 - np.min(curve1)) / (np.max(curve1) - np.min(curve1))
normalized_curve2 = (curve2 - np.min(curve2)) / (np.max(curve2) - np.min(curve2))

# 正規化された曲線をプロット
plt.plot(p, normalized_curve1, color='blue')
plt.plot(p, normalized_curve2, color='red')



# 以降のプロットや計算はそのまま続けても良い
# DTW距離を計算
distance, path = fastdtw(curve1, curve2)
# 正規化された曲線を使用してDTW距離を計算
distance_normalized, path_normalized = fastdtw(normalized_curve1, normalized_curve2)

    
plt.ylim(-0.5, 1.5)  # 正規化後の範囲に合わせて調整
plt.legend()
plt.show()


print(f"DTW距離: {distance}")
print(f"DTW距離(正規化後): {distance_normalized}")