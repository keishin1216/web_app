import matplotlib.pyplot as plt
import numpy as np
import math

N = 5000
xmin = 0
xmax = 106



def f(a,b,x):
    return (a*np.exp(-(((x/3)-(b/3))**2/2)))/(math.sqrt(2*math.pi))
#a = h
#b = t
def g(x):
    return f(1,11,x)+f(2,12,x)+f(1,14,x)+f(3,17,x)+f(3,19,x)+f(3,19,x)+f(3,21,x)+f(1,22,x)+f(2,25,x)+f(3,26,x)+f(1,27,x)+f(1,29,x)+f(1,29,x)+f(1,31,x)+f(2,34,x)+f(1,36,x)+f(2,37,x)+f(2,41,x)+f(3,42,x)+f(3,44,x)+f(3,46,x)+f(2,47,x)+f(2,50,x)+f(3,52,x)+f(1,53,x)+f(1,55,x)+f(3,56,x)+f(3,56,x)+f(2,57,x)+f(3,58,x)+f(2,60,x)+f(1,64,x)+f(1,64,x)+f(1,71,x)+f(3,72,x)+f(2,73,x)+f(1,73,x)+f(1,76,x)+f(1,78,x)+f(3,80,x)+f(3,85,x)+f(1,87,x)+f(3,89,x)+f(1,93,x)+f(1,94,x)+f(2,94,x)+f(1,97,x)



p = np.linspace(xmin, xmax, N)

plt.plot(p, g(p))



import matplotlib.pyplot as plt

ymin, ymax = 0, 6

plt.vlines(10, ymin, ymax, colors='black', linestyle='dashed', linewidth=3)
plt.ylim(ymin, ymax)
plt.vlines(65, ymin, ymax, colors='black', linestyle='dashed', linewidth=3)
plt.ylim(ymin, ymax)
plt.vlines(71, ymin, ymax, colors='black', linestyle='dashed', linewidth=3)
plt.ylim(ymin, ymax)
plt.vlines(101, ymin, ymax, colors='black', linestyle='dashed', linewidth=3)
plt.ylim(ymin, ymax)


plt.vlines(13, ymin, ymax, colors='red', linestyle='dashed', linewidth=1)
plt.ylim(ymin, ymax)
plt.vlines(21, ymin, ymax, colors='red', linestyle='dashed', linewidth=1)
plt.ylim(ymin, ymax)
plt.vlines(28, ymin, ymax, colors='red', linestyle='dashed', linewidth=1)
plt.ylim(ymin, ymax)
plt.vlines(38, ymin, ymax, colors='red', linestyle='dashed', linewidth=1)
plt.ylim(ymin, ymax)
plt.vlines(46, ymin, ymax, colors='red', linestyle='dashed', linewidth=1)
plt.ylim(ymin, ymax)
plt.vlines(55, ymin, ymax, colors='red', linestyle='dashed', linewidth=1)
plt.ylim(ymin, ymax)
plt.vlines(64, ymin, ymax, colors='red', linestyle='dashed', linewidth=1)
plt.ylim(ymin, ymax)
plt.vlines(72, ymin, ymax, colors='red', linestyle='dashed', linewidth=1)
plt.ylim(ymin, ymax)


plt.show()


