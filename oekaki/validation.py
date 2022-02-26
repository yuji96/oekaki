import re
import warnings
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import oekaki

UNIT_BRACKET = "(", ")"


def show(level: str = "error"):
    validate(plt.gcf(), level)
    plt.show()


class MisleadingWarning(DeprecationWarning):
    pass


class validate:

    def __init__(self, fig: Figure, level: Literal["error", "warning", "ignore"]):
        if level not in {"error", "warning", "ignore"}:
            raise ValueError(
                'invalid level. choose from "error", "warning", or "ignore".')

        self.fig = fig
        self.warnings = []

        level = level.replace("warning", "always")
        warnings.simplefilter(level, MisleadingWarning)
        self.validate()

    def validate(self):
        for ax in self.fig.get_axes():
            if not ax.has_data():
                continue
            self.validate_labels(ax)
        if self.warnings:
            warnings.warn(
                "".join(f'\n{w["label"]}: {w["msg"]}' for w in self.warnings),
                MisleadingWarning, stacklevel=5)

    def validate_labels(self, ax: Axes):
        _1, _2 = oekaki.UNIT_BRACKET
        label = ax.get_label()

        for var in ["x", "y"]:
            target = getattr(ax, f"get_{var}label")()
            if not target:
                self.warnings.append({"label": label, "msg": f"No {var}-label."})
            elif not re.search(f".*\\{_1}.*\\{_2}", target):
                # TODO: English
                self.warnings.append({"label": label, "msg": f"No {var}-unit."})

            getattr(ax, f"set_{var}label")(target.replace(f"{_1}{_2}", ""))
