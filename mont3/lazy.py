from __future__ import annotations

from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
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
        self.lazyaxes: list[tuple[tuple, LazyAxes]] = []
        self.mode = Mode.NONE
        self.strict = strict

    def __getitem__(self, key) -> LazyAxes:
        if self.mode is Mode.SINGLE:
            raise TypeError("Single mode is selected."
                            " In single mode, this object is not subscriptable."
                            " ex) fig.plot(...)")
        if not isinstance(key, (int, tuple, slice)):
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
        elif isinstance(key, slice):
            return Mode.NONE
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
        pos, lazyaxes = zip(*self.lazyaxes)

        # FIXME: 縦一列のときにNoneが入ってるっぽい？
        tuples = filter(lambda obj: isinstance(obj, tuple), pos)
        rmax, cmax = map(lambda nums: max(nums) + 1, zip(*tuples))
        fig, axes = plt.subplots(rmax, cmax)

        if isinstance(axes, Axes):
            axes = np.array(axes)
        axes = axes.reshape(rmax, cmax)

        # TODO: refactor
        slices = []
        for r_c, lazy_ax in zip(pos, lazyaxes):
            if lazy_ax.kind is None:
                continue
            if isinstance(r_c, slice):
                slices.append((r_c, lazy_ax))
                continue

            getattr(axes[r_c], lazy_ax.kind)(*lazy_ax.args, **lazy_ax.kwargs)

        unique_axes = fig.get_axes()
        for ax in unique_axes:
            if ax.has_data():
                ax.grid(True)
        for r_c, lazy_ax in slices:
            for ax in unique_axes[r_c]:
                getattr(ax, lazy_ax.kind)(*lazy_ax.args, **lazy_ax.kwargs)

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
