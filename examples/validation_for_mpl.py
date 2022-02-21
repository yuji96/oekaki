import matplotlib.pyplot as plt
import numpy as np
import oekaki

x = np.linspace(0, 2 * np.pi, 50)

fig, ax = plt.subplots(1, 1)
ax.plot(x, np.sin(x))
oekaki.show(strict=True)

fig, ax = plt.subplots(1, 2)
ax[1].plot(x, np.sin(x))
oekaki.show()

fig, ax = plt.subplots(2, 2)
ax[1, 1].plot(x, np.sin(x))
oekaki.show()
