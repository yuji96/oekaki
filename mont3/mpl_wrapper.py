from __future__ import annotations

from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from .validation import validate


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
        if not isinstance(key, (int, tuple)):
            raise TypeError("Specify an integer or"
                            " an integer sequence of length 2.")
        if isinstance(key, tuple) and len(key) != 2:
            raise ValueError("Specify an integer or"
                             " an integer sequence of length 2.")

        if self.dim is None:
            self.dim = self.init_getitem(key)

        if self.dim == 1:
            if not isinstance(key, int):
                raise TypeError("Line mode is selected. Specify an integer."
                                " ex) fig[0].plot(...)")

            key = (0, key)
        elif self.dim == 2:
            if not isinstance(key, tuple):
                raise TypeError("Table mode is selected."
                                " Specify an integer sequence of length 2."
                                " ex) fig[0, 0].plot(...)")

        ax = LazyAxes()
        self.lazyaxes.append((key, ax))
        return ax

    def init_getitem(self, key):
        if isinstance(key, int):
            return 1
        elif isinstance(key, tuple):
            return 2
        else:
            raise TypeError("Specify an integer or"
                            " an integer sequence of length 2.")

    def __getattribute__(self, name):
        if name not in dir(Axes):
            return super().__getattribute__(name)

        if self.dim is None:
            self.dim = 0
        if self.dim != 0:
            raise AttributeError(
                "Single mode is selected. Get axes via indices. ex) fig[0].plot(...)"
            )
        ax = LazyAxes()
        self.lazyaxes.append(((0, 0), ax))
        return getattr(ax, name)

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
