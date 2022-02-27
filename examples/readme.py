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
