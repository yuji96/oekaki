from .mpl_wrapper import *  # noqa
import matplotlib.pyplot as plt
import japanize_matplotlib  # noqa

def show(*args, **kwargs):
    return plt.show(*args, **kwargs)
