import numpy as np
import oekaki

x = np.linspace(0, 2 * np.pi, 50)

# FIXME
# fig = oekaki.figure(strict=False)
# fig.plot(x, np.sin(x))
# fig.show()

fig = oekaki.figure(strict=False)
fig[:].plot(x, np.cos(x))
fig[1].plot(x, np.sin(x))
fig.show()

fig = oekaki.figure(strict=False)
fig[:].plot(x, np.cos(x))
fig[1, 1].plot(x, np.sin(x))
fig.show()
