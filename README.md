# Oekaki

Lazy on demand subplots.

# Features

- 1️⃣ You can add subplots later, wherever you want.
- 2️⃣ You can manipulate subplots with numpy-like slices.
- 3️⃣ Oekaki warn about potentially misleading graphs. (ex: No labels or units.)
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

- [matplotlib](https://pypi.org/project/matplotlib/)

# Installation

```
pip install oekaki
```
If you want to also install [japanize-matplotlib](https://pypi.org/project/japanize-matplotlib/), run below.
```
pip install "oekaki[ja]"
```

# Usage

Under construction.

# Note

Under construction.

# Author

Under construction.

# License

Under construction.
