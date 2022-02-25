import numpy as np
import oekaki


fig = oekaki.figure(constrained_layout=True, level="warning")
fig["bar"].bar(["a", "b", "c"], [5, 7, 9])
fig["plot"].plot([1, 2, 3])
fig["hist"].hist(np.random.rand(100))
fig["image"].imshow([[1, 2], [2, 1]])

fig.show("""bar  | plot
            hist | hist """)
