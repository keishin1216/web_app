from fastdtw import fastdtw
from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

# CSVファイルからデータを読み込む
df1 = pd.read_csv('../plus_data.csv/馬場.csv')
df2 = pd.read_csv('../eda改/1月 eda 馬場.csv')

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

# DataFrameから必要な列を取得
x2 = df2['time(min)']
y2 = df2['buttonNumber']

spots = ['E', 'F', 'D', 'B', 'C', 'A', 'G']
spot_times = [10, 10, 10, 20, 7, 5, 40]
move_times = [0, 1, 8, 1, 3, 2, 3]

# 曲線をプロット
N = 5000
xmin = 0
xmax = 120  # x軸の範囲を0から120に変更
ymin, ymax = -5, 15
x_spot = 0
p = np.linspace(xmin, xmax, N)
curve1 = g(p, df1['buttonNumber'].values, df1['time(min)'].values)
interp_func = interp1d(x2.values, y2.values, bounds_error=False, fill_value=(x2.values[0], x2.values[-1]))
curve2 = interp_func(p)

for spot, spot_time, move_time in zip(spots, spot_times, move_times):
    y_spot = g(x_spot + spot_time, df1['buttonNumber'].values, df1['time(min)'].values)
    
    # Add vertical lines for each spot with black dashed lines
    plt.vlines(x_spot + move_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    plt.vlines(x_spot + move_time + spot_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    
    # Add label for each spot
    plt.text(x_spot + move_time + spot_time / 2, ymax, spot, verticalalignment='bottom', horizontalalignment='center', fontsize=12, color='red')
    
    x_spot += move_time + spot_time

# Adjust Y-axis range
#plt.ylim(ymin, ymax)

time_values_original = df1['time(min)'].values

# curve1 と curve2 を正規化
normalized_curve1 = (curve1 - np.min(curve1)) / (np.max(curve1) - np.min(curve1))
normalized_curve2_smooth = (curve2 - np.min(curve2)) / (np.max(curve2) - np.min(curve2))
#window_size_curve2 = 10
#normalized_curve2_smooth = pd.Series(normalized_curve2_smooth).rolling(window_size_curve2).mean().bfill().values[:len(normalized_curve1)]





plt.figure(figsize=(10, 5))

# 正規化された曲線とピークをプロットする
plt.subplot(1, 2, 1)
# 正規化された曲線をプロット
plt.plot(p, normalized_curve1, label='Normalized IEL')
plt.plot(p, normalized_curve2_smooth, label='Normalized EDA')

# DTW距離を計算
distance, path = fastdtw(curve1, curve2)
distance_normalized, path_normalized = fastdtw(normalized_curve1, normalized_curve2_smooth)
for spot, spot_time, move_time in zip(spots, spot_times, move_times):
    x_spot_original = np.sum(move_times[:spots.index(spot)+1]) + np.sum(spot_times[:spots.index(spot)])
    plt.vlines(x_spot_original, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    plt.vlines(x_spot_original + spot_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    plt.text(x_spot_original + spot_time / 2, 1.5, spot, verticalalignment='bottom', horizontalalignment='center', fontsize=12, color='red')
# ピークを見つける
peaks_curve1, _ = find_peaks(normalized_curve1)
peaks_curve2, _ = find_peaks(normalized_curve2_smooth)

# ピークのy座標とそのx座標を取得
peak_y_curve1 = normalized_curve1[peaks_curve1]
peak_x_curve1 = p[peaks_curve1]

peak_y_curve2 = normalized_curve2_smooth[peaks_curve2]
peak_x_curve2 = p[peaks_curve2]

# 最小ピークを見つける
min_peaks_curve1, _ = find_peaks(-normalized_curve1)  # 負のピークを見つけるためにy値を反転
min_peaks_curve2, _ = find_peaks(-normalized_curve2_smooth)

# 最小ピークのy座標とそのx座標を取得
min_peak_y_curve1 = normalized_curve1 [min_peaks_curve1]  # 再度反転
min_peak_x_curve1 = p[min_peaks_curve1]

min_peak_y_curve2 = normalized_curve2_smooth[min_peaks_curve2]  # 再度反転
min_peak_x_curve2 = p[min_peaks_curve2]

# 1番目から3番目までのピークと最小ピークの情報を取得
top_n_peaks_curve1 = [(x, y) for y, x in sorted(zip(peak_y_curve1, peak_x_curve1), reverse=True)[:3]]
top_n_peaks_curve2 = [(x, y) for y, x in sorted(zip(peak_y_curve2, peak_x_curve2), reverse=True)[:3]]

top_n_min_peaks_curve1 = [(x, y) for y, x in sorted(zip(min_peak_y_curve1, min_peak_x_curve1), reverse=False)[:3]]
top_n_min_peaks_curve2 = [(x, y) for y, x in sorted(zip(min_peak_y_curve2, min_peak_x_curve2), reverse=False)[:3]]



# ピークと最小ピークをプロット
for i, (x, y) in enumerate(top_n_peaks_curve1):
    plt.scatter(x, y, marker='x', color='blue', label='max' if i == 0 else None)  # max1, max2, max3

for i, (x, y) in enumerate(top_n_peaks_curve2):
    plt.scatter(x, y, marker='x', color='red', label=None)  # max1, max2, max3

for i, (x, y) in enumerate(top_n_min_peaks_curve1):
    plt.scatter(x, y, marker='o', color='blue', label='min' if i == 0 else None)  # min1, min2, min3

for i, (x, y) in enumerate(top_n_min_peaks_curve2):
    plt.scatter(x, y, marker='o', color='red', label=None)  # min1, min2, min3

plt.legend()  # 一度だけラベルを表示


plt.xlabel('Time (min)')
plt.ylabel('Normalized Values')

# 結果を出力
print("IEL Peaks:")
print("Top3 Peaks (x, y):", top_n_peaks_curve1)
print("\nEDA Peaks:")
print("Top 3 Peaks (x, y):", top_n_peaks_curve2)

print("\nIEL Min Peaks:")
print("Top 3 Min Peaks (x, y):", top_n_min_peaks_curve1)
print("\nEDA Min Peaks:")
print("Top 3 Min Peaks (x, y):", top_n_min_peaks_curve2)

plt.ylim(-0.5, 1.5)  # 正規化後の範囲に合わせて調整
#plt.legend()
#plt.show()
plt.subplot(1, 2, 2)
plt.plot(p, normalized_curve1, label='Normalized IEL')
plt.plot(p, normalized_curve2_smooth, label='Normalized EDA')
for spot, spot_time, move_time in zip(spots, spot_times, move_times):
    x_spot_original = np.sum(move_times[:spots.index(spot)+1]) + np.sum(spot_times[:spots.index(spot)])
    plt.vlines(x_spot_original, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    plt.vlines(x_spot_original + spot_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    plt.text(x_spot_original + spot_time / 2, 1.5, spot, verticalalignment='bottom', horizontalalignment='center', fontsize=12, color='red')
# ピークの総数を計算
total_peaks_curve1 = len(peaks_curve1) + len(min_peaks_curve1)
total_peaks_curve2 = len(peaks_curve2) + len(min_peaks_curve2)

print("Total Peaks IEL:", total_peaks_curve1)
print("Total Peaks EDA:", total_peaks_curve2)

# すべてのピークをプロット
for x, y in zip(peak_x_curve1, peak_y_curve1):
    plt.scatter(x, y, marker='x', color='blue')

for x, y in zip(peak_x_curve2, peak_y_curve2):
    plt.scatter(x, y, marker='x', color='red')

for x, y in zip(min_peak_x_curve1, min_peak_y_curve1):
    plt.scatter(x, y, marker='o', color='blue')

for x, y in zip(min_peak_x_curve2, min_peak_y_curve2):
    plt.scatter(x, y, marker='o', color='red')
plt.legend()
# ラベルを設定
plt.xlabel('Time (min)')
plt.ylabel('Normalized Values')
plt.ylim(-0.5, 1.5)

plt.tight_layout()
# グラフを表示
plt.show()


print(f"DTW距離: {distance}")
print(f"DTW距離(正規化後): {distance_normalized}")
correlation_coefficient, _ = pearsonr(normalized_curve1, normalized_curve2_smooth)
print(f"相関係数: {correlation_coefficient}")
