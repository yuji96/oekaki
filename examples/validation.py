import matplotlib.pyplot as plt
import numpy as np
import oekaki

x = np.linspace(0, 2 * np.pi, 50)

fig, ax = plt.subplots(1, 1)
ax.plot(x, np.sin(x))
oekaki.show(level="ignore")

fig, ax = plt.subplots(1, 1)
ax.plot(x, np.sin(x))
oekaki.show(level="warning")

fig, ax = plt.subplots(1, 1)
ax.plot(x, np.sin(x))
oekaki.show(level="error")
