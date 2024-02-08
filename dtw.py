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


spots = ['A', 'B', 'C', 'D', 'E', 'F']
spot_times = [20, 15, 10, 10, 10, 30]
move_times = [5, 4, 3, 8, 2, 3]

# 曲線をプロット
N = 5000
xmin = 0
xmax = 120
ymin, ymax = -5, 15
x_spot = 0
p = np.linspace(xmin, xmax, N)
curve1 = g(p, df1['buttonNumber'].values, df1['time(min)'].values)
curve2 = g(p, df2['buttonNumber'].values, df2['time(min)'].values)

#plt.plot(p, curve1, label='IEL')
#plt.plot(p, curve2, label='EDA')
for spot, spot_time, move_time in zip(spots, spot_times, move_times):
    y_spot = g(x_spot + spot_time, df1['buttonNumber'].values, df1['time(min)'].values)
    
    # Add vertical lines for each spot with black dashed lines
    plt.vlines(x_spot + move_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    plt.vlines(x_spot + move_time + spot_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    
    # Add label for each spot
    plt.text(x_spot + move_time + spot_time / 2, ymax, spot, verticalalignment='bottom', horizontalalignment='center', fontsize=12, color='red')
    
    x_spot += move_time + spot_time

plt.ylim(ymin, ymax)
#plt.legend()
#plt.show()
# 既存のプロットコード

time_values_original = df1['time(min)'].values


# curve1 と curve2 を正規化
normalized_curve1 = (curve1 - np.min(curve1)) / (np.max(curve1) - np.min(curve1))
normalized_curve2 = (curve2 - np.min(curve2)) / (np.max(curve2) - np.min(curve2))

# 正規化された曲線をプロット
plt.plot(p, normalized_curve1, label='Normalized IEL')
plt.plot(p, normalized_curve2, label='Normalized EDA')



# 以降のプロットや計算はそのまま続けても良い
# DTW距離を計算
distance, path = fastdtw(curve1, curve2)
# 正規化された曲線を使用してDTW距離を計算
distance_normalized, path_normalized = fastdtw(normalized_curve1, normalized_curve2)

for spot, spot_time, move_time in zip(spots, spot_times, move_times):
    x_spot_original = np.sum(move_times[:spots.index(spot)+1]) + np.sum(spot_times[:spots.index(spot)])
    plt.vlines(x_spot_original, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    plt.vlines(x_spot_original + spot_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    plt.text(x_spot_original + spot_time / 2, 1.5, spot, verticalalignment='bottom', horizontalalignment='center', fontsize=12, color='red')

x_values_curve1 = p
x_values_curve2 = p
y_values_curve1 = normalized_curve1
y_values_curve2 = normalized_curve2

from scipy.signal import find_peaks

# ピークを見つける
peaks_curve1, _ = find_peaks(y_values_curve1)
peaks_curve2, _ = find_peaks(y_values_curve2)

# ピークのy座標とそのx座標を取得
peak_y_curve1 = y_values_curve1[peaks_curve1]
peak_x_curve1 = x_values_curve1[peaks_curve1]

peak_y_curve2 = y_values_curve2[peaks_curve2]
peak_x_curve2 = x_values_curve2[peaks_curve2]

# 最小ピークを見つける
min_peaks_curve1, _ = find_peaks(-y_values_curve1)  # 負のピークを見つけるためにy値を反転
min_peaks_curve2, _ = find_peaks(-y_values_curve2)

# 最小ピークのy座標とそのx座標を取得
min_peak_y_curve1 = -y_values_curve1[min_peaks_curve1]  # 再度反転
min_peak_x_curve1 = x_values_curve1[min_peaks_curve1]

min_peak_y_curve2 = -y_values_curve2[min_peaks_curve2]  # 再度反転
min_peak_x_curve2 = x_values_curve2[min_peaks_curve2]

# 1番目から3番目までのピークと最小ピークの情報を取得
n = 3  # 上位3つのピークを取得
top_n_peaks_curve1 = list(zip(peak_x_curve1[:n], peak_y_curve1[:n]))
top_n_peaks_curve2 = list(zip(peak_x_curve2[:n], peak_y_curve2[:n]))

top_n_min_peaks_curve1 = list(zip(min_peak_x_curve1[:n], min_peak_y_curve1[:n]))
top_n_min_peaks_curve2 = list(zip(min_peak_x_curve2[:n], min_peak_y_curve2[:n]))
plt.figure(figsize=(10, 6))

# ピークをプロット
for i, (x, y) in enumerate(top_n_peaks_curve1):
    plt.scatter(x, y, marker='x', color='red', label=f'max{i+1}')  # max1, max2, max3

for i, (x, y) in enumerate(top_n_peaks_curve2):
    plt.scatter(x, y, marker='x', color='blue', label=f'max{i+1}')  # max1, max2, max3

# 最小ピークをプロット
for i, (x, y) in enumerate(top_n_min_peaks_curve1):
    plt.scatter(x, y, marker='o', color='green', label=f'min{i+1}')  # min1, min2, min3

for i, (x, y) in enumerate(top_n_min_peaks_curve2):
    plt.scatter(x, y, marker='o', color='orange', label=f'min{i+1}')  # min1, min2, min3
plt.plot(p, normalized_curve1, label='Normalized IEL', color='red')
plt.plot(p, normalized_curve2, label='Normalized EDA', color='blue')
plt.xlabel('X Values')
plt.ylabel('Y Values')
# 結果を出力
print("Curve 1 Peaks:")
print("Top 3 Peaks (x, y):", top_n_peaks_curve1)
print("\nCurve 2 Peaks:")
print("Top 3 Peaks (x, y):", top_n_peaks_curve2)

print("\nCurve 1 Min Peaks:")
print("Top 3 Min Peaks (x, y):", top_n_min_peaks_curve1)
print("\nCurve 2 Min Peaks:")
print("Top 3 Min Peaks (x, y):", top_n_min_peaks_curve2)

plt.ylim(-0.5, 1.5)  # 正規化後の範囲に合わせて調整
plt.legend()
plt.show()



print(f"DTW距離: {distance}")
print(f"DTW距離(正規化後): {distance_normalized}")
correlation_coefficient, _ = pearsonr(normalized_curve1, normalized_curve2)
print(f"相関係数: {correlation_coefficient}")

# 平均絶対誤差の計算
#mae = np.mean(np.abs(normalized_curve1, normalized_curve2))
#print(f"平均絶対誤差 (MAE): {mae}")



