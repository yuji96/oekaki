import mont3 as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 50)

fig = plt.figure()
fig.plot(x, np.sin(x))
fig.show()

fig = plt.figure()
fig[1].plot(x, np.sin(x))
fig.show()

fig = plt.figure()
fig[1, 1].plot(x, np.sin(x))
fig.show()
