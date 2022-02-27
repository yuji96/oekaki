import inspect
import itertools
import re
from typing import overload

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.axes import Axes

from .validation import validate

support_seaborn = []
for name in dir(sns):
    func = getattr(sns, name)
    if callable(func) and "ax" in inspect.signature(func).parameters:
        support_seaborn.append(name)


class LazyAxes(Axes):

    attrs = ["attr", "next", "args", "kwargs"]
    methods = [
        "reverse", "sns", "seaborn", "_ipython_canary_method_should_not_exist_"
    ]

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

    def __repr__(self):
        return f"<LazyAxes: {self.attr}>"

    def __iter__(self):
        yield self

    def reverse(self, ax):
        lazy_ax = self
        while lazy_ax:
            if lazy_ax.attr == "seaborn":
                lazy_ax = lazy_ax.next
                func = lazy_ax.attr
                if func not in support_seaborn:
                    raise ValueError(
                        f"{func} is not suppoted. choose form {support_seaborn}")

                lazy_ax.kwargs["ax"] = ax
                ax = getattr(sns, func)(*lazy_ax.args, **lazy_ax.kwargs)
            else:
                ax = getattr(ax, lazy_ax.attr)
                if lazy_ax.args or lazy_ax.kwargs:
                    ax = ax(*lazy_ax.args, **lazy_ax.kwargs)
            lazy_ax = lazy_ax.next
        return ax

    @property
    def seaborn(self) -> sns:
        if sns is None:
            raise ModuleNotFoundError("No module named 'seaborn'.")

        self.attr = "seaborn"
        return self

    @property
    def sns(self, *args, **kwargs) -> sns:
        return self.seaborn(*args, **kwargs)


class figure:

    def __init__(self, level: str = "warning", **kwargs):
        self.level = level
        self.kwargs = kwargs

        self.keys: list[str] = []
        self.lazyaxes: list[LazyAxes] = []
        self.lazyattrs: list[LazyAxes] = []

    def __getattr__(self, name):
        fig_attr = LazyAxes(name)
        self.lazyattrs.append(fig_attr)
        return fig_attr

    def __getitem__(self, label: str) -> LazyAxes:
        if not isinstance(label, str):
            raise KeyError("support str only.")
        ax = LazyAxes()
        self.keys.append(label)
        self.lazyaxes.append(ax)
        return ax

    def draw(self, mosaic):
        mosaic = convert_mosaic(mosaic)
        chain = set(itertools.chain(*mosaic))

        fig = plt.figure(**self.kwargs)
        ax_dict = fig.subplot_mosaic(mosaic)

        for key, lazy_ax in zip(self.keys, self.lazyaxes):
            for match_key in filter(re.compile(key).search, chain):
                lazy_ax.reverse(ax_dict[match_key])

        for fig_attr in self.lazyattrs:
            fig_attr.reverse(fig)

        validate(fig, level=self.level)
        return fig

    def show(self, mosaic):
        self.draw(mosaic)
        # TODO: これをオブジェクト指向的にやる方法って無いのかな
        plt.show()

    def save(self, filename):
        self.draw()
        plt.savefig(filename)

    def __str__(self):
        return f"<figure: {id(self)}>"


def convert_mosaic(mosaic):
    if isinstance(mosaic, str) and "|" in mosaic:
        return [[cell.strip() for cell in line.split("|")]
                for line in mosaic.splitlines()]
    return mosaic
