import numpy as np
from app.utils import ml
from scipy.special import erfc


def test_ml_a_1():
    z = np.linspace(-2, 2, 50)
    assert np.allclose(ml(z, a=1, b=1), np.exp(z))


def test_ml_a_2():
    z = np.linspace(-2, 2, 50)
    assert np.allclose(ml(z ** 2, a=2, b=1), np.cosh(z))


def test_ml_a_05():
    z = np.linspace(0, 2, 50)
    assert np.allclose(ml(np.sqrt(z), a=0.5, b=1), np.exp(z) * erfc(-np.sqrt(z)))
