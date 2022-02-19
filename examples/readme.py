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
