import numpy as np
from scipy.integrate import quad
from scipy.special import gamma


def float_pow(x, y):
    return (np.sign(x) * np.abs(x)) ** y


def intg(func, a, b, *args, **kwargs):
    return quad(func, a, b, *args, **kwargs)[0]


def ml(z, a, b):
    k = np.arange(0, 28).reshape(-1, 1)
    E = float_pow(z, k) / gamma(a * k + b)
    return np.sum(E, axis=0)
