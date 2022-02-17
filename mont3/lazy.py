from __future__ import annotations

from enum import Enum

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from .validation import validate


class Mode(Enum):
    NONE = -1
    SINGLE = 0
    LINE = 1
    TABLE = 2


class LazyAxes(Axes):

    attrs = ["kind", "args", "kwargs", "__str__"]

    def __init__(self):
        self.kind: str = None
        self.args = []
        self.kwargs = {}

    def __getattribute__(self, name: str):
        if name == "attrs" or name in self.attrs:
            return super().__getattribute__(name)

        def store(*args, **kwargs):
            self.kind = name
            self.args = args
            self.kwargs = kwargs

        return store

    def __str__(self):
        return f"<LazyAxes: {self.kind}>"


class figure(Axes):

    def __init__(self, strict=True):
        self.lazyaxes = []
        self.mode = Mode.NONE
        self.strict = strict

    def __getitem__(self, key) -> LazyAxes:
        if self.mode is Mode.SINGLE:
            raise TypeError("Single mode is selected."
                            " In single mode, this object is not subscriptable."
                            " ex) fig.plot(...)")
        if not isinstance(key, (int, tuple)):
            raise TypeError("Specify an integer or"
                            " an integer sequence of length 2.")
        if isinstance(key, tuple) and len(key) != 2:
            raise ValueError("Specify an integer or"
                             " an integer sequence of length 2.")

        if self.mode is Mode.NONE:
            self.mode = self.init_getitem(key)

        if self.mode is Mode.LINE:
            if not isinstance(key, int):
                raise TypeError("Line mode is selected. Specify an integer."
                                " ex) fig[0].plot(...)")
            key = (0, key)
        elif self.mode is Mode.TABLE:
            if not isinstance(key, tuple):
                raise TypeError("Table mode is selected."
                                " Specify an integer sequence of length 2."
                                " ex) fig[0, 0].plot(...)")

        ax = LazyAxes()
        self.lazyaxes.append((key, ax))
        return ax

    def init_getitem(self, key):
        if isinstance(key, int):
            return Mode.LINE
        elif isinstance(key, tuple):
            return Mode.TABLE
        else:
            raise TypeError("Specify an integer or"
                            " an integer sequence of length 2.")

    def __getattribute__(self, name):
        if name not in dir(Axes):
            return super().__getattribute__(name)

        if self.mode is Mode.NONE:
            self.mode = Mode.SINGLE
        if self.mode is not Mode.SINGLE:
            raise AttributeError("Single mode is selected."
                                 " Get axes via indices. ex) fig[0].plot(...)")
        ax = LazyAxes()
        self.lazyaxes.append(((0, 0), ax))
        return getattr(ax, name)

    def _draw(self):
        pos, graphes = zip(*self.lazyaxes)

        rmax, cmax = map(lambda nums: max(nums) + 1, zip(*pos))
        fig, axes = plt.subplots(rmax, cmax)
        for (r, c), graph in zip(pos, graphes):
            if (rmax, cmax) == (1, 1):
                ax = axes
            elif rmax == 1:
                ax = axes[c]
            else:
                ax = axes[r, c]
            getattr(ax, graph.kind)(*graph.args, **graph.kwargs)
            ax.grid(True)

        validate(fig, strict=self.strict)
        return fig, axes

    def show(self):
        self._draw()
        # TODO: これをオブジェクト指向的にやる方法って無いのかな
        plt.tight_layout()
        plt.show()

    def save(self, filename):
        self._draw()
        plt.tight_layout()
        plt.savefig(filename)

    def __str__(self):
        return f"<figure: {id(self)}>"
