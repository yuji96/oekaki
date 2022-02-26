import warnings
from pathlib import Path

import matplotlib
import numpy as np
import oekaki
import seaborn as sns
from oekaki.validation import MisleadingWarning
from pytest import PytestUnknownMarkWarning

from tests.utils import compare_figures

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa

warnings.simplefilter("ignore", (MisleadingWarning, PytestUnknownMarkWarning))

path = Path(__file__).parent.joinpath("failed_cases")
[p.unlink() for p in path.glob("*.png") if p.is_file()]

x = np.linspace(0, 2 * np.pi, 50)


@compare_figures
def test_single():
    mosaic = "A"
    expected = plt.figure()
    ax_dict = expected.subplot_mosaic(mosaic)
    ax_dict["A"].bar(["a", "b", "c"], [5, 7, 9])

    actual = oekaki.figure(level="ignore")
    actual["A"].bar(["a", "b", "c"], [5, 7, 9])
    actual = actual._draw(mosaic)
    return expected, actual


@compare_figures
def test_line():
    mosaic = "AB"
    expected = plt.figure()
    ax_dict = expected.subplot_mosaic(mosaic)
    ax_dict["A"].bar(["a", "b", "c"], [5, 7, 9])
    ax_dict["B"].plot([1, 2, 3])

    actual = oekaki.figure(level="ignore")
    actual["A"].bar(["a", "b", "c"], [5, 7, 9])
    actual["B"].plot([1, 2, 3])
    actual = actual._draw(mosaic)
    return expected, actual


@compare_figures
def test_table():
    mosaic = "AB\nCD"
    rand = np.random.rand(100)

    expected = plt.figure()
    ax_dict = expected.subplot_mosaic(mosaic)
    ax_dict["A"].bar(["a", "b", "c"], [5, 7, 9])
    ax_dict["B"].plot([1, 2, 3])
    ax_dict["C"].hist(rand)
    ax_dict["D"].imshow([[1, 2], [2, 1]])

    actual = oekaki.figure(level="ignore")
    actual["A"].bar(["a", "b", "c"], [5, 7, 9])
    actual["B"].plot([1, 2, 3])
    actual["C"].hist(rand)
    actual["D"].imshow([[1, 2], [2, 1]])
    actual = actual._draw(mosaic)
    return expected, actual


@compare_figures
def test_sns():
    mosaic = "AB"
    expected = plt.figure()
    ax_dict = expected.subplot_mosaic(mosaic)
    ax_dict["A"].bar(["a", "b", "c"], [5, 7, 9])
    sns.lineplot(data=[1, 2, 3], ax=ax_dict["B"])

    actual = oekaki.figure(level="ignore")
    actual["A"].bar(["a", "b", "c"], [5, 7, 9])
    actual["B"].sns.lineplot(data=[1, 2, 3])
    actual = actual._draw(mosaic)
    return expected, actual


@compare_figures
def _test_table_all_slice():
    expected, axes = plt.subplots(2, 2, squeeze=False)
    for ax in axes.reshape(-1):
        ax.set(xlabel="あ", ylabel="い")
    axes[1, 1].plot(x, np.sin(x))

    actual = oekaki.figure(level="ignore")
    actual[:].set(xlabel="あ", ylabel="い")
    actual[1, 1].plot(x, np.sin(x))
    actual, axes = actual._draw()
    return expected, actual


# TODO: test validations
