# Oekaki

matplotlib extension for me (... and you).

## Features

1. Oekaki warn about potentially misleading graphs. (ex: No labels or units.)
2. You can manipulate subplots with numpy-like slices.
3. You can add subplots later, wherever you want.
4. (Oekaki imports `japanize-matplotlib` if it's installed.)

# Demo

img

```python
import numpy as np
import oekaki

theta = np.linspace(0, np.pi, 300)
r = np.abs(np.tan(theta))**(1 / np.abs(np.tan(theta)))

fig = oekaki.figure(strict=False)
fig[:, 0].set(facecolor="black")
fig[0, :].grid(True)
fig[1, 1].fill(r * np.cos(theta), r * np.sin(theta), color="#2ce62c")
fig[1, 1].set(aspect="equal", title="俺流 matplotlib")
fig.show()
# out:
# examples/readme.py:20: Mont3Warning:
# (1, 1): No x-label.
# (1, 1): No y-label.
```

---

# Requirement

- matplotlib

# Installation

```
pip install git+git@github.com:yuji96/mont3.git
# in the future, `pip install oekaki`
```

# Usage

Under construction.

# Note

Under construction.

# Author

Under construction.

# License

Under construction.
