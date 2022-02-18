import warnings
from pathlib import Path

import matplotlib
import mont3
import numpy as np
from mont3.validation import Mont3Warning
from pytest import PytestUnknownMarkWarning

from tests.utils import compare_figures

matplotlib.use('Agg')
from matplotlib import pyplot  # noqa

warnings.simplefilter("ignore", (Mont3Warning, PytestUnknownMarkWarning))

path = Path(__file__).parent.joinpath("failed_cases")
[p.unlink() for p in path.glob("*.png") if p.is_file()]

x = np.linspace(0, 2 * np.pi, 50)


@compare_figures
def test_single():
    expected, ax = pyplot.subplots(1, 1)
    ax.plot(x, np.sin(x))
    ax.set(xlabel="あ", ylabel="い")

    actual = mont3.figure(strict=False)
    actual.plot(x, np.sin(x))
    actual.set(xlabel="あ", ylabel="い")
    actual, _ = actual._draw()
    return expected, actual


@compare_figures
def test_line():
    expected, axes = pyplot.subplots(1, 2)
    ax = axes[1]
    ax.plot(x, np.sin(x))
    ax.set(xlabel="あ", ylabel="い")

    actual = mont3.figure(strict=False)
    actual[1].plot(x, np.sin(x))
    actual[1].set(xlabel="あ", ylabel="い")
    actual, _ = actual._draw()
    return expected, actual


@compare_figures
def test_table():
    expected, axes = pyplot.subplots(2, 2)
    ax = axes[1, 1]
    ax.plot(x, np.sin(x))
    ax.set(xlabel="あ", ylabel="い")

    actual = mont3.figure(strict=False)
    actual[1, 1].plot(x, np.sin(x))
    actual[1, 1].set(xlabel="あ", ylabel="い")
    actual, _ = actual._draw()
    return expected, actual


@compare_figures
def test_table_all_slice():
    expected, axes = pyplot.subplots(2, 2, squeeze=False)
    for ax in axes.reshape(-1):
        ax.set(xlabel="あ", ylabel="い")
    axes[1, 1].plot(x, np.sin(x))

    actual = mont3.figure(strict=False)
    actual[:].set(xlabel="あ", ylabel="い")
    actual[1, 1].plot(x, np.sin(x))
    actual, axes = actual._draw()
    return expected, actual


# TODO: test validations
