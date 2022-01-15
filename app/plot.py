import matplotlib.pyplot as plt
import numpy as np

from main import function

q = 1.2
lam = 2
T = 5


def f(s):
    return np.sin(s)


step = 0.1
t_range = np.arange(0, T + step, step, dtype=np.float64)

x_t = []
for t in t_range:
    x_t.append(function(t, T, lam, q, f))

x_t = np.array(x_t)

plt.rcParams.update({"font.size": 24})

plt.plot(t_range, x_t, "r", linewidth=4)

plt.grid()
plt.show()
