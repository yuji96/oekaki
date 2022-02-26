import numpy as np
import oekaki

fig = oekaki.figure(tight_layout=True, level="warning")
fig["bar"].bar(["a", "b", "c"], [5, 7, 9])
fig["image"].imshow([[1, 2], [2, 1]])
fig["line"].sns.lineplot(data=np.random.rand(100))
fig["hist"].sns.histplot(data=np.random.rand(100))

fig["line"].set(xlabel="time (sec)", ylabel="voltage (mV)")

fig.show("""bar  | image
            line | hist """)
