from .mpl_wrapper import *  # noqa
from .validation import *  # noqa
import matplotlib.pyplot as plt
import japanize_matplotlib  # noqa

def show(strict=True):
    validate(plt.gcf(), strict)
    plt.show()
