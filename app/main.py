from typing import Callable, Union

import numpy as np

from .utils import float_pow, intg, ml

Number = Union[int, float, np.number]


def function(
    t: Number,
    lam: Number,
    q: Number,
    T: Number,
    f: Callable,
) -> Number:
    def func_t_s_1(s):
        lTs = lam * float_pow(T - s, q)
        return float_pow(T - s, q - 1) * ml(lTs, a=q, b=q) * f(s)

    def func_t_s_2(s):
        lTs = lam * float_pow(T - s, q)
        return float_pow(T - s, q - 2) * ml(lTs, a=q, b=q - 1) * f(s)

    def func_t_s_3(s):
        return float_pow(t - s, q - 1) * ml(lam * float_pow(t - s, q), a=q, b=q) * f(s)

    lTq = lam * float_pow(T, q)

    return (
        (1 - ml(lTq, a=q, b=1))
        * intg(func_t_s_1, 0, T)
        * ml(lam * float_pow(t, q), a=q, b=1)
        + T
        * ml(lTq, a=q, b=2)
        * intg(func_t_s_2, 0, T)
        * ml(lam * float_pow(t, q), a=q, b=1)
        + (1 - ml(lTq, a=q, b=1))
        * intg(func_t_s_2, 0, T)
        * t
        * ml(lam * float_pow(t, q), a=q, b=2)
        + float_pow(float(T), -1)
        * ml(lTq, a=q, b=0)
        * intg(func_t_s_1, 0, T)
        * t
        * ml(lam * float_pow(t, q), a=q, b=2)
    ) / (
        float_pow(1 - ml(lTq, a=q, b=1), 2) - ml(lTq, a=q, b=0) * ml(lTq, a=q, b=2)
    ) + intg(
        func_t_s_3,
        0,
        t,
    )
