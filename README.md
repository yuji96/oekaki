# Oekaki

Lazy on demand subplots.

# Features

- 1️⃣ You can draw subplots, wherever and whenever you want.
- 2️⃣ You can access mosaic subplots with Regex.
- 3️⃣ Oekaki warn about potentially misleading graphs. (No labels or units.) This feature can be ignored.
- 🍣 (Oekaki imports `japanize-matplotlib` if it's installed.)

# Demo

<img src="https://raw.githubusercontent.com/yuji96/oekaki/main/examples/readme.png" width="500px" >

```python
import numpy as np
import oekaki

# 1️⃣: lazy draw subplots
fig = oekaki.figure(tight_layout=True)

# 2️⃣: able to use regex search
fig["left"].set(facecolor="black")
fig["upper"].grid(True)

# 🍣 japanize
fig["lower right"].set(aspect="equal", title="俺流 matplotlib")

theta = np.linspace(0, np.pi, 300)
r = np.abs(np.tan(theta))**(1 / np.abs(np.tan(theta)))
fig["lower right"].fill(r * np.cos(theta), r * np.sin(theta), color="#2ce62c")
fig.show("""upper left | upper right
            lower left | lower right""")
```

3️⃣: This code raises the following warnings.

```
example/readme.py:12: MisleadingWarning:
lower right: No x-label.
lower right: No y-label.
  fig.show("""upper left | upper right
```

# Requirement

- [matplotlib](https://matplotlib.org/stable/)
- [seaborn](https://seaborn.pydata.org/)

# Installation

```
pip install oekaki
```

If you want to also install [japanize-matplotlib](https://github.com/uehara1414/japanize-matplotlib), run below.

```
pip install "oekaki[ja]"
```

# Usage

First, create a figure instance.

```python
fig = oekaki.figure()
```

You can use [all matplotlib's Axes API](https://matplotlib.org/stable/api/axes_api.html).

```python
fig["plot"].plot(x, y)
```

You can also use some [seaborn API](https://seaborn.pydata.org/api.html) through `sns` property. They must have `ax` argument.

```python
fig["hist"].sns.histplot(data=data)
```

It is also possible to manipulate the subplots using regex. (This is implemented using [re.Pattern.search](https://docs.python.org/3/library/re.html#re.Pattern.search).)

```python
# `.*` means ALL
fig[".*"].grid(True)
```

Finally, let's draw it in (enhanced) [Mosaic format](https://matplotlib.org/stable/tutorials/provisional/mosaic.html)!
```python
fig.show("""hist | plot""")
fig.show("""hist
            plot""")
```

# Note

Under construction.

# Author

Under construction.

# License

Under construction.
