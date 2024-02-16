from fastdtw import fastdtw
from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
# CSVファイルからデータを読み込む
df1 = pd.read_csv('../plus_data.csv/みどり 高村.csv')
df2 = pd.read_csv('../eda改/1月 eda 高村.csv')

# ... (previous code remains unchanged)
N = 5000
xmin = 0
xmax = 140
ymin, ymax = -5, 15
x_spot = 0
p = np.linspace(xmin, xmax, N)
# Iterate over different values of i
for i in range(1, 9):
    print(f"Calculating DTW distances for i={i}...")
    
    # Define the function f with the current value of i
    def f(a, b, x):
        c = i
        return (a * np.exp(-(((x / c) - (b / c))**2 / 2))) / (math.sqrt(2 * math.pi))
    def g(x, a_values, b_values):
     result = np.zeros_like(x, dtype=np.float64)
     for a, b in zip(a_values, b_values):
        result += f(a, b, x)
     return result

    # Recalculate the curves with the updated function f
    curve1 = g(p, df1['buttonNumber'].values, df1['time(min)'].values)
    curve2 = g(p, df2['buttonNumber'].values, df2['time(min)'].values)

    # Normalize the curves
    normalized_curve1 = (curve1 - np.min(curve1)) / (np.max(curve1) - np.min(curve1))
    normalized_curve2 = (curve2 - np.min(curve2)) / (np.max(curve2) - np.min(curve2))

    # Calculate DTW distances
   
    distance_normalized, _ = fastdtw(normalized_curve1, normalized_curve2)

    # Print the results for each value o
    print(f"DTW距離(正規化後) (i={i}): {distance_normalized}")
    
    # ... (continue with other calculations or plots if needed)
