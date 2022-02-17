import warnings
import re

from matplotlib.axes import Axes
from matplotlib.figure import Figure


class Mont3Warning(DeprecationWarning):
    pass


class validate:

    def __init__(self, fig: Figure, strict):
        self.fig = fig

        if strict:
            warnings.simplefilter('error', Mont3Warning)
        self.validate()

    def validate(self):
        for i, ax in enumerate(self.fig.get_axes()):
            self.validate_labels(ax)
        warnings.warn("set below", Mont3Warning, stacklevel=4)

    def validate_labels(self, ax: Axes):
        for var in ["x", "y"]:
            target = getattr(ax, f"get_{var}label")()
            if not target:
                warnings.warn("ラベルがない", stacklevel=5)
            elif not re.search(r'\[.*\]', target):
                warnings.warn("単位がない", stacklevel=5)
            getattr(ax, f"set_{var}label")(target.replace("[]", ""))
