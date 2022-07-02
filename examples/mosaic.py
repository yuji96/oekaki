import numpy as np
import oekaki

fig = oekaki.figure(tight_layout=True, level="warning")
fig[".*"].grid(True)
fig[".*"].set(axisbelow=True)
fig[r"a|1"].set(facecolor="lightblue")

fig["a"].bar(["a", "b", "c"], [5, 7, 9])
fig["b"].imshow([[1, 2], [2, 1]])
fig["1"].sns.lineplot(data=np.random.rand(100))
fig["2"].sns.histplot(data=np.random.rand(100))

fig.suptitle("hoge")
fig.show("""a | b
            1 | 2 """)
