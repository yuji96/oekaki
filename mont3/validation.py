import warnings
import re
import matplotlib.pyplot as plt

from matplotlib.axes import Axes
from matplotlib.figure import Figure


def show(strict=True):
    validate(plt.gcf(), strict)
    plt.show()


class Mont3Warning(DeprecationWarning):
    pass


class validate:

    def __init__(self, fig: Figure, strict):
        self.fig = fig
        self.warnings = []

        if strict:
            warnings.simplefilter('error', Mont3Warning)
        self.validate()

    def validate(self):
        for ax in self.fig.get_axes():
            if not ax.has_data():
                continue
            self.validate_labels(ax)
        warnings.warn("".join(f'\n{w["geo"]}: {w["msg"]}' for w in self.warnings),
                      Mont3Warning,
                      stacklevel=4)

    def validate_labels(self, ax: Axes):
        # TODO: 関数の外側にする？
        geo = self.calc_geometry(ax)
        for var in ["x", "y"]:
            target = getattr(ax, f"get_{var}label")()
            if not target:
                self.warnings.append({"geo": geo, "msg": f"{var}ラベルがない"})
            elif not re.search(r'\[.*\]', target):
                self.warnings.append({"geo": geo, "msg": "単位がない"})

            getattr(ax, f"set_{var}label")(target.replace("[]", ""))

    @staticmethod
    def calc_geometry(ax):
        _, n_cols, i, _ = ax.get_subplotspec().get_geometry()
        return divmod(i, n_cols)
