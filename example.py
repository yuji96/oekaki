import mont3 as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 50)
fig = plt.figure()
fig[0].plot(x, np.sin(x))
fig[1].scatter(x, np.cos(x))
# TODO: 上書きできるようにしたい
# fig[0].plot(x, np.sin(x))
fig.show()

x = np.linspace(0, 4 * np.pi, 50)
fig = plt.figure()
fig[0, 0].plot(x, np.sin(x))
fig[1, 1].plot(x, np.cos(x))
fig.show()

plt.show()
