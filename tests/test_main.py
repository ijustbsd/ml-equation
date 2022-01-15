from typing import Callable

import numpy as np
from app.main import Number, function
from app.utils import float_pow, intg, ml


def function_f_s(
    t: np.array,
    lam: Number,
    q: Number,
    T: Number,
    **kwargs,
):
    lTq = lam * float_pow(T, q)

    return (
        -(1 - ml(lTq, a=q, b=1))
        / (
            float_pow((1 - ml(lTq, a=q, b=1)), 2)
            - ml(lTq, a=q, b=0) * ml(lTq, a=q, b=2)
        )
        * ((T * ml(lam * float_pow(t, q), a=q, b=1)) / lam)
        - ml(lTq, a=q, b=0)
        / (
            float_pow((1 - ml(lTq, a=q, b=1)), 2)
            - ml(lTq, a=q, b=0) * ml(lTq, a=q, b=2)
        )
        * ((t * ml(lam * float_pow(t, q), a=q, b=2)) / lam)
        - t / lam
    )


def function_f_1(
    t: np.array,
    lam: Number,
    q: Number,
    T: Number,
    f: Callable,
):
    def f_1(t, s):
        return -(
            float_pow(np.e, -np.sqrt(lam) * np.abs(t - s))
            + float_pow(np.e, -np.sqrt(lam) * (T - np.abs(t - s)))
        ) / (2 * np.sqrt(lam) * (1 - float_pow(np.e, -np.sqrt(lam) * T)))

    def integrand(s, t):
        return f_1(t, s) * f(s)

    return intg(integrand, 0, T, args=(t,))


def test_function_f_s(function_params_f_s):
    t_linspace = np.linspace(0, function_params_f_s["T"], 10)

    x_t = []
    x_t_s = []
    for t in t_linspace:
        x_t.append(function(t, **function_params_f_s))
        x_t_s.append(function_f_s(t, **function_params_f_s))
    x_t = np.array(x_t)
    x_t_s = np.array(x_t_s)

    np.testing.assert_allclose(x_t, x_t_s)


def test_function_f_1(function_params_f_1):
    t_linspace = np.linspace(0, function_params_f_1["T"], 10)

    x_t = []
    x_t_1 = []
    for t in t_linspace:
        x_t.append(function(t, **function_params_f_1))
        x_t_1.append(function_f_1(t, **function_params_f_1))
    x_t = np.array(x_t)
    x_t_1 = np.array(x_t_1)

    np.testing.assert_allclose(x_t.flat, x_t_1.flat)
