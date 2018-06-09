import numpy as np
k = 4
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

y = [0.01444,
     0.01520,
     39.70696,
     40.88858,
     0.14414,
     0.14357,
     405.23399,
     404.30444,
     0.07892,
     0.08707,
     0.17324,
     0.162020,
     0.47991,
     0.46382,
     1.30784,
     1.31269]

x = np.array(x)
y = np.array(y)
b = np.zeros((k,));
b = [sum([x[i][j]*y[i] for i in range(N)])/N for j in range(k)]
print(b)


