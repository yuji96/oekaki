# Oekaki

matplotlib extension for me (... and you).

# Features

- 1️⃣ You can add subplots later, wherever you want.
- 2️⃣ You can manipulate subplots with numpy-like slices.
- 3️⃣ Oekaki warn about potentially misleading graphs. (ex: No labels or units.)
- 🍣 (Oekaki imports `japanize-matplotlib` if it's installed.)

# Demo

img

```python
import numpy as np
import oekaki

# 1️⃣: lazy draw subplots
fig = oekaki.figure(strict=False)

# 2️⃣: able to use slice
fig[:, 0].set(facecolor="black")
fig[0, :].grid(True)


# 🍣 japanize
fig[1, 1].set(aspect="equal", title="俺流 matplotlib")

theta = np.linspace(0, np.pi, 300)
r = np.abs(np.tan(theta))**(1 / np.abs(np.tan(theta)))
fig[1, 1].fill(r * np.cos(theta), r * np.sin(theta), color="#2ce62c")
fig.show()
# out:
# examples/readme.py:20: Mont3Warning:
# (1, 1): No x-label.
# (1, 1): No y-label.
```

3️⃣: This code raises the following warnings.

```
examples/readme.py:16: Mont3Warning: 
(1, 1): No x-label.
(1, 1): No y-label.
  fig.show()
```

# Requirement

- matplotlib

# Installation

```
pip install git+git@github.com:yuji96/oekaki.git
# in the future, `pip install oekaki`
```

todo: `oekaki[ja]`

# Usage

Under construction.

# Note

Under construction.

# Author

Under construction.

# License

Under construction.
