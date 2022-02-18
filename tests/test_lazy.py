import warnings

import matplotlib
import mont3
import numpy as np
from mont3.validation import Mont3Warning
from pytest import PytestUnknownMarkWarning

from tests.utils import compare_figures

matplotlib.use('Agg')
from matplotlib import pyplot  # noqa

warnings.simplefilter("ignore", (Mont3Warning, PytestUnknownMarkWarning))

x = np.linspace(0, 2 * np.pi, 50)


@compare_figures
def test_single():
    expected, ax = pyplot.subplots(1, 1)
    ax.plot(x, np.sin(x))
    ax.grid(True)
    ax.set(xlabel="あ", ylabel="い")

    actual = mont3.figure(strict=False)
    actual.plot(x, np.sin(x))
    actual.set(xlabel="あ", ylabel="い")
    actual, axes = actual._draw()
    return expected, actual


@compare_figures
def test_line():
    expected, axes = pyplot.subplots(1, 2)
    ax = axes[1]
    ax.plot(x, np.sin(x))
    ax.grid(True)
    ax.set(xlabel="あ", ylabel="い")

    actual = mont3.figure(strict=False)
    actual[1].plot(x, np.sin(x))
    actual[1].set(xlabel="あ", ylabel="い")
    actual, axes = actual._draw()
    return expected, actual


@compare_figures
def test_table():
    expected, axes = pyplot.subplots(2, 2)
    ax = axes[1, 1]
    ax.plot(x, np.sin(x))
    ax.grid(True)
    ax.set(xlabel="あ", ylabel="い")

    actual = mont3.figure(strict=False)
    actual[1, 1].plot(x, np.sin(x))
    actual[1, 1].set(xlabel="あ", ylabel="い")
    actual, axes = actual._draw()
    return expected, actual


# TODO: test validations
