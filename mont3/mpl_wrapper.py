from matplotlib.axes import Axes
import matplotlib.pyplot as plt


class LazyAxes(Axes):

    def __init__(self, *args, **kwargs):
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

    def __repr__(self):
        return f"<LazyAxes: {self.kind}>"


class figure:

    def __init__(self):
        # TODO: rename lazyaxes
        self.graphes = []
        self.mode = None

    def __getitem__(self, key) -> LazyAxes:
        # TODO: 分けたほうがよい？
        if isinstance(key, int):
            if self.mode == "table":
                raise ValueError(
                    "You have selected table mode. Specify an integer sequence of length 2."
                )
            elif self.mode is None:
                self.mode = "line"

            # for line layout
            ax = LazyAxes()
            self.graphes.append(((0, key), ax))
            return ax

        elif isinstance(key, tuple):
            if self.mode == "line":
                raise ValueError("You have selected line mode. Specify an integer.")
            elif self.mode is None:
                self.mode = "table"

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
            ax = axes[r, c] if rmax == 2 else axes[c]
            getattr(ax, graph.kind)(*graph.args, **graph.kwargs)
            ax.grid(True)

        fig.show(*args, **kwargs)
        plt.tight_layout()
        plt.show()
