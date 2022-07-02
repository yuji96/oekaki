import matplotlib.pyplot as plt
import numpy as np
import oekaki
import seaborn as sns

x = np.linspace(0, 2 * np.pi, 50)

fig, ax = plt.subplots(1, 1, constrained_layout=True)
ax.plot(x, np.sin(x), label="A")
sns.scatterplot(x=x, y=np.cos(x))
ax.set(xlabel="時刻", ylabel=r"電圧 ($\mu V$)")
# ax.grid(True)
ax.legend()
oekaki.show(level="warning")
