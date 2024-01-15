import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

# Read data from CSV file
df = pd.read_csv('../eda改/Book1.csv')  # Replace 'your_data_file.csv' with your actual file name
a_values = df['buttonNumber'].values
b_values = df['time(min)'].values

N = 5000
xmin = 0
xmax = 140

def f(a, b, x):
    return (a * np.exp(-(((x / 3) - (b / 3))**2 / 2))) / (math.sqrt(2 * math.pi))

def g(x, a_values, b_values):
    result = np.zeros_like(x, dtype=np.float64)
    for a, b in zip(a_values, b_values):
        result += f(a, b, x)
    return result

p = np.linspace(xmin, xmax, N)


spots = ['A', 'B', 'C', 'D', 'E', 'F']
spot_times = [20, 15, 10, 10, 10, 30]
move_times = [5, 4, 3, 8, 2, 3]

# Plot the curve using data from CSV
plt.plot(p, g(p, a_values, b_values))

ymin, ymax = -5, 15
x_spot = 0
for spot, spot_time, move_time in zip(spots, spot_times, move_times):
    y_spot = g(x_spot + spot_time, a_values, b_values)
    
    # Add vertical lines for each spot with black dashed lines
    plt.vlines(x_spot + move_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1, label=f'Stay at {spot}')
    plt.vlines(x_spot + move_time + spot_time, ymin, ymax, colors='black', linestyle='dashed', linewidth=1)
    
    # Add label for each spot
    plt.text(x_spot + move_time + spot_time / 2, ymax, spot, verticalalignment='bottom', horizontalalignment='center', fontsize=12, color='red')
    
    x_spot += move_time + spot_time

# Set y-axis limits
plt.ylim(ymin, ymax)

# Show the plot
plt.show()