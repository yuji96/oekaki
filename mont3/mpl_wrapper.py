from __future__ import annotations
import warnings

from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


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
        # FIXME: ここが無視されてる
        return f"<LazyAxes: {self.kind}>"


class figure(Axes):

    def __init__(self, strict=True):
        self.lazyaxes = []
        self.dim = None
        self.strict = strict

    def __getitem__(self, key) -> LazyAxes:
        if self.dim == 0:
            raise TypeError("Single mode is selected."
                            " In single mode, this object is not subscriptable."
                            " ex) fig.plot(...)")

        if isinstance(key, int):
            if self.dim == 2:
                raise ValueError("Table mode is selected."
                                 " Specify an integer sequence of length 2."
                                 " ex) fig[0, 0].plot(...)")
            elif self.dim is None:
                self.dim = 1

            # for line layout
            ax = LazyAxes()
            self.lazyaxes.append(((0, key), ax))
            return ax

        elif isinstance(key, tuple):
            if self.dim == 1:
                raise ValueError("Line mode is selected. Specify an integer."
                                 " ex) fig[0].plot(...)")
            elif self.dim is None:
                self.dim = 2

            if len(key) != 2:
                raise ValueError("Specify an integer or"
                                 " an integer sequence of length 2.")

            # for table layout
            ax = LazyAxes()
            self.lazyaxes.append((key, ax))
            return ax

        else:
            raise TypeError("Specify an integer or"
                            " an integer sequence of length 2.")

    def __getattribute__(self, name):
        if name in dir(Axes):
            if self.dim is None:
                self.dim = 0
            if self.dim != 0:
                raise AttributeError(
                    "Single mode is selected. Get axes via indices. ex) fig[0].plot(...)"
                )
            ax = LazyAxes()
            self.lazyaxes.append(((0, 0), ax))
            return getattr(ax, name)
        return super().__getattribute__(name)

    def show(self, filename=None, *args, **kwargs):
        pos, graphes = zip(*self.lazyaxes)

        rmax, cmax = 0, 0
        for r, c in pos:
            rmax = r if rmax < r else rmax
            cmax = c if cmax < c else cmax
        rmax += 1
        cmax += 1

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

        plt.tight_layout()
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)

    def __str__(self):
        return f"<figure: {id(self)}>"


class Mont3Warning(DeprecationWarning):
    pass


def validate(fig: Figure, strict=True):
    if strict:
        warnings.simplefilter('error', Mont3Warning)

    check_list = ["xlabel", "ylabel"]

    all_results = {}
    for i, ax in enumerate(fig.get_axes()):
        results = []
        for check in check_list:
            if not getattr(ax, f"get_{check}")():
                results.append(check)
        if results:
            all_results[i] = results

    warnings.warn(f"set below\n\t{str(all_results)}", Mont3Warning, stacklevel=3)
