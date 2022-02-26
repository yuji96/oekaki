from typing import Hashable, Tuple, overload

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from plum import dispatch

from .validation import validate


class LazyAxes(Axes):

    attrs = ["attr", "next", "args", "kwargs"]
    methods = ["reverse"]

    def __init__(self, attr=None):
        self.attr = attr
        self.next = None
        self.args = []
        self.kwargs = {}

    def __getattribute__(self, attr):
        if attr in ["attrs", "methods"]:
            return super().__getattribute__(attr)
        if attr in self.attrs + self.methods:
            return super().__getattribute__(attr)

        if self.attr is None:
            self.attr = attr
            return self
        else:
            self.next = LazyAxes(attr)
            return self.next

    def __call__(self, *args, **kwargs):
        self.is_called = True
        self.args = args
        self.kwargs = kwargs
        return self

    def __str__(self):
        return f"<LazyAxes: {self.attr}>"

    def reverse(self, ax):
        lazy_ax = self
        while lazy_ax:
            ax = getattr(ax, lazy_ax.attr)
            if lazy_ax.args or lazy_ax.kwargs:
                ax = ax(*lazy_ax.args, **lazy_ax.kwargs)
            lazy_ax = lazy_ax.next
        return ax


class figure:

    def __init__(self, level: str, **kwargs):
        self.level = level
        self.kwargs = kwargs

        self.lazyaxes: list[Tuple[Hashable, LazyAxes]] = []

    @overload
    @dispatch
    def __getitem__(self, label: str) -> LazyAxes:
        ax = LazyAxes()
        self.lazyaxes.append((label, ax))
        return ax

    @dispatch
    def __getitem__(self, key) -> None:
        raise NotImplementedError

    def _draw(self, mosaic):

        fig = plt.figure(**self.kwargs)
        ax_dict = fig.subplot_mosaic(convert_mosaic(mosaic))

        for key, lazy_ax in self.lazyaxes:
            try:
                lazy_ax.reverse(ax_dict[key])
            except KeyError:
                pass

        validate(fig, level=self.level)
        return fig

    def show(self, mosaic):
        self._draw(mosaic)
        # TODO: これをオブジェクト指向的にやる方法って無いのかな
        plt.show()

    def save(self, filename):
        self._draw()
        plt.savefig(filename)

    def __str__(self):
        return f"<figure: {id(self)}>"


def convert_mosaic(mosaic):
    if isinstance(mosaic, str) and "|" in mosaic:
        return [[cell.strip() for cell in line.split("|")]
                for line in mosaic.splitlines()]
    return mosaic
