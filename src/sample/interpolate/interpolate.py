import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
x = np.arange(0, 10)
# y = np.exp(-x / 3.0)
y = [100,123,456, 220, 123, 223, 321, 222, 456, 456]
f = interpolate.interp1d(x, y, 'slinear')

poloinomial_coeffitients = np.polyfit(x, y, 1)
poly_function = np.poly1d(poloinomial_coeffitients)
line = poly_function(x)
print(poly_function(0))
xnew = np.arange(0, 9, 0.1)
ynew = f(xnew)  # use interpolation function returned by `interp1d`
plt.plot(x, y, 'o', xnew, ynew, '-')
plt.plot(line, 'r-')
plt.show()

