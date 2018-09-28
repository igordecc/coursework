import numpy as np
import matplotlib.pyplot as plt
k = 3
N = 2**k

#x = [[ for j in range(k)] for i in range(N)]
a = np.ndarray((2**k, k))
cur = 2**(k -1 )
for i in range(a.shape[1]):
    for j in range(a.shape[0]):
        a[j][i] = -1 if (j // cur) % 2 == 0 else 1
    cur >>= 1
print(a)
x = a
"""
x = [[-1,-1,-1,-1],
     [-1,-1,-1, 1],
     [-1,-1, 1,-1],
     [-1,-1, 1 ,1],
     [-1, 1,-1,-1],
     [-1, 1,-1, 1],
     [-1, 1, 1,-1],
     [-1, 1, 1, 1],
     [1, -1, -1, -1],
     [1, -1, -1, 1],
     [1, -1, 1, -1],
     [1, -1, 1, 1],
     [1, 1, -1, -1],
     [1, 1, -1, 1],
     [1, 1, 1, -1],
     [1, 1, 1, 1],
     ]
"""

y = [0.02908,
     22.56792,
     0.16434,
     227.47706,
     0.07892,
     0.17324,
     0.47991,
     1.30784]

x = np.array(x)
y = np.array(y)
b = np.zeros((k,));
b = [sum([x[i][j]*y[i] for i in range(N)])/N for j in range(k)]
print(b)


plt.bar(np.arange(1, k+1),b)
ax = plt.axes()
ax.yaxis.grid()
ax.set_xticks(np.arange(1,k+1))
plt.xlabel("фактор j")
plt.ylabel("коэффициент bj")
plt.show()
