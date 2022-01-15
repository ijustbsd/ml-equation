import pytest


@pytest.fixture()
def function_params_f_s():
    q = 1.2
    lam = 2
    T = 5

    def f(s):
        return s

    return {
        "q": q,
        "lam": lam,
        "T": T,
        "f": f,
    }


@pytest.fixture()
def function_params_f_1():
    q = 2
    lam = 2
    T = 2

    def f(_):
        return 1

    return {
        "q": q,
        "lam": lam,
        "T": T,
        "f": f,
    }
