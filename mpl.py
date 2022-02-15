import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 50)

fig, ax = plt.subplots(1, 2)
ax[0].plot(x, np.sin(x))
ax[1].scatter(x, np.cos(x))
ax[0].plot(x, np.cos(x))
fig.show()

x = np.linspace(0, 4 * np.pi, 50)
fig, ax = plt.subplots(2, 2)
ax[0, 0].plot(x, np.sin(x))
ax[1, 1].scatter(x, np.cos(x))
fig.show()

plt.show()
