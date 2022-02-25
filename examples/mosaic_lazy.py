import numpy as np
import oekaki


fig = oekaki.figure(constrained_layout=True, strict=False)
fig["bar"].bar(["a", "b", "c"], [5, 7, 9])
fig["plot"].plot([1, 2, 3])
fig["hist"].hist(np.random.rand(100))
# fig["image"].imshow([[1, 2], [2, 1]])

hoge = """bar  | plot
          hist | image """
hoge = [[cell.strip() for cell in line.split("|")] for line in hoge.splitlines()]
fig.show(hoge)
