from __future__ import annotations
from matplotlib.axes import Axes
import matplotlib.pyplot as plt


class LazyAxes(Axes):

    def __init__(self):
        self.kind: str = None
        self.args = []
        self.kwargs = {}

    def __getattribute__(self, name: str):

        def store(*args, **kwargs):
            self._store(name, args, kwargs)

        if name in dir(Axes):
            return store

        return super().__getattribute__(name)

    def _store(self, kind, args, kwargs):
        self.kind = kind
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        # FIXME: ここが無視されてる
        return f"<LazyAxes: {self.kind}>"


class figure(Axes):

    def __init__(self):
        # TODO: rename lazyaxes
        self.graphes = []
        self.dim = None

    def __getitem__(self, key) -> LazyAxes:
        if self.dim == 0:
            raise TypeError(
                "Single mode is selected. In single mode, this object is not subscriptable. ex) fig.plot(...)"
            )

        if isinstance(key, int):
            if self.dim == 2:
                raise ValueError(
                    "Table mode is selected. Specify an integer sequence of length 2. ex) fig[0, 0].plot(...)"
                )
            elif self.dim is None:
                self.dim = 1

            # for line layout
            ax = LazyAxes()
            self.graphes.append(((0, key), ax))
            return ax

        elif isinstance(key, tuple):
            if self.dim == 1:
                raise ValueError("Line mode is selected. Specify an integer. ex) fig[0].plot(...)")
            elif self.dim is None:
                self.dim = 2

            if len(key) != 2:
                raise ValueError(
                    "Specify an integer or an integer sequence of length 2.")

            # for table layout
            ax = LazyAxes()
            self.graphes.append((key, ax))
            return ax

        else:
            raise TypeError(
                "Specify an integer or an integer sequence of length 2.")

    def __getattribute__(self, name):
        if name in dir(Axes):
            if self.dim is None:
                self.dim = 0
            if self.dim != 0:
                raise AttributeError(
                    "Single mode is selected. Get axes via indices. ex) fig[0].plot(...)"
                )
            ax = LazyAxes()
            self.graphes.append(((0, 0), ax))
            return getattr(ax, name)
        return super().__getattribute__(name)

    def show(self, *args, **kwargs):
        pos, graphes = zip(*self.graphes)

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

        fig.show(*args, **kwargs)
        plt.tight_layout()
        plt.show()

    def __str__(self):
        return f"<figure: {id(self)}>"