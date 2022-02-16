import re
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
            target = getattr(ax, f"get_{check}")()
            if not target:
                results.append([check, f"without {check}"])
            elif "label" in check and \
                    not re.search(r'\[.*\]', target):
                results.append([check, f"without unit."])
            getattr(ax, f"set_{check}")(target.replace("[]", ""))

        if results:
            all_results[i] = results

    warnings.warn(f"set below\n\t{str(all_results)}", Mont3Warning, stacklevel=3)
