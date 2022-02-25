from enum import Enum
from typing import Union, overload

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from plum import dispatch

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

        # TODO: <store:> って表示されるの直したい
        return store

    def __str__(self):
        return f"<LazyAxes: {self.kind}>"


class figure:

    def __init__(self, strict=True, **kwargs):
        self.strict = strict
        self.kwargs = kwargs

        self.lazyaxes: list[tuple[Union[tuple, str], LazyAxes]] = []

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
            # if not lazy_ax.kind:
            #     continue

            try:
                getattr(ax_dict[key], lazy_ax.kind)(*lazy_ax.args, **lazy_ax.kwargs)
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
