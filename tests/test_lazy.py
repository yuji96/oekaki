import inspect
import warnings

import matplotlib
import mont3
import numpy as np
from matplotlib.testing.compare import calculate_rms
from mont3.validation import Mont3Warning
from pytest import PytestUnknownMarkWarning

from tests.utils import convert_to_ndarray, save_diff_image

matplotlib.use('Agg')
from matplotlib import pyplot  # noqa

warnings.simplefilter("ignore", (Mont3Warning, PytestUnknownMarkWarning))

x = np.linspace(0, 2 * np.pi, 50)


def test_hoge():
    # TODO: test validations
    warnings.simplefilter("ignore", Mont3Warning)

    expected, axes = pyplot.subplots(1, 1)
    axes.plot(x, np.sin(x))
    axes.grid(True)
    axes.set(xlabel="あ", ylabel="い")

    actual = mont3.figure(strict=False)
    actual.plot(x, np.sin(x))
    actual.set(xlabel="あ", ylabel="い")
    actual, axes = actual._draw()

    expected_img, actual_img = map(convert_to_ndarray, [expected, actual])

    res = calculate_rms(expected_img, actual_img)
    if res > 0:
        cf = inspect.currentframe()
        name = inspect.getframeinfo(cf).function
        save_diff_image(expected_img, actual_img, f"tests/failed_cases/{name}.png")
        raise AssertionError
