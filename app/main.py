from typing import Callable, Union

import numpy as np

from .utils import float_pow, intg, ml

Number = Union[int, float, np.number]


def function_q_01(
    t: Number,
    C: Number,
    lam: Number,
    q: Number,
    T: Number,
    f: Callable,
) -> list[Number]:
    def func_t_s(s):
        lTs = lam * float_pow(t - s, q)
        return float_pow(t - s, q - 1) * ml(lTs, a=q, b=q) * f(s)

    return C * ml(lam * float_pow(t, q), a=q, b=1) + intg(func_t_s, 0, t)


def function_q_1(
    t: Number,
    C: Number,
    lam: Number,
    q: Number,
    T: Number,
    f: Callable,
) -> list[Number]:
    def func_e(s):
        return float_pow(np.e, lam * (t - s)) * f(s)

    return [C * float_pow(np.e, lam * t) + intg(func_e, 0, t)]


def function_q_12(
    t: Number,
    C1: Number,
    C2: Number,
    lam: Number,
    q: Number,
    T: Number,
    f: Callable,
) -> list[Number]:
    def func_t_s(s):
        lTs = lam * float_pow(t - s, q)
        return float_pow(t - s, q - 1) * ml(lTs, a=q, b=q) * f(s)

    return (
        C1 * ml(lam * float_pow(t, q), a=q, b=1)
        + C2 * t * ml(lam * float_pow(t, q), a=q, b=2)
        + intg(func_t_s, 0, t)
    )


def function_q_2(
    t: Number,
    C1: Number,
    C2: Number,
    lam: Number,
    q: Number,
    T: Number,
    f: Callable,
) -> list[Number]:
    def func_e(s):
        return (
            float_pow(np.e, np.sqrt(lam) * (t - s))
            - float_pow(np.e, -np.sqrt(lam) * (t - s))
        ) * f(s)

    return [
        C1
        * (float_pow(np.e, np.sqrt(lam) * t) + float_pow(np.e, -np.sqrt(lam) * t))
        / 2
        + 1
        / np.sqrt(lam)
        * C2
        * (float_pow(np.e, np.sqrt(lam) * t) - float_pow(np.e, -np.sqrt(lam) * t))
        / 2
        + 1 / (2 * np.sqrt(lam)) * intg(func_e, 0, t),
    ]


def function(
    t: Number,
    C: Number,
    C1: Number,
    C2: Number,
    lam: Number,
    q: Number,
    T: Number,
    f: Callable,
) -> list[Number]:

    if 0 < q < 1:
        return function_q_01(t=t, C=C, lam=lam, q=q, T=T, f=f)
    elif q == 1:
        return function_q_1(t=t, C=C, lam=lam, q=q, T=T, f=f)
    elif 1 < q < 2:
        return function_q_12(t=t, C1=C1, C2=C2, lam=lam, q=q, T=T, f=f)
    elif q == 2:
        return function_q_2(t=t, C1=C1, C2=C2, lam=lam, q=q, T=T, f=f)
    else:
        raise ValueError
