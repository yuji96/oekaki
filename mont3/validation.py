import warnings
from matplotlib.figure import Figure


class Mont3Warning(DeprecationWarning):
    pass


def validate(fig: Figure, strict=True):
    if strict:
        warnings.simplefilter('error', Mont3Warning)

    check_list = ["xlabel", "ylabel"]

    all_results = {}
    for i, ax in enumerate(fig.get_axes()):
        results = []
        for check in check_list:
            if not getattr(ax, f"get_{check}")():
                results.append(check)
        if results:
            all_results[i] = results

    warnings.warn(f"set below\n\t{str(all_results)}", Mont3Warning, stacklevel=3)
