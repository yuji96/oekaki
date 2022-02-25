import re
import warnings
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


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
                "".join(f'\n{w["geo"]}: {w["msg"]}' for w in self.warnings),
                MisleadingWarning, stacklevel=5)

    def validate_labels(self, ax: Axes):
        # TODO: 関数の外側にする？
        geo = self.calc_geometry(ax)
        for var in ["x", "y"]:
            target = getattr(ax, f"get_{var}label")()
            if not target:
                self.warnings.append({"geo": geo, "msg": f"No {var}-label."})
            elif not re.search(r'\[.*\]', target):
                # TODO: English
                self.warnings.append({"geo": geo, "msg": "単位がない"})

            getattr(ax, f"set_{var}label")(target.replace("[]", ""))

    @staticmethod
    def calc_geometry(ax):
        _, n_cols, i, _ = ax.get_subplotspec().get_geometry()
        return divmod(i, n_cols)
