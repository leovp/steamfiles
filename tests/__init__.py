from collections import OrderedDict


def sort_dict(d):
    """
    Helper function; returns a recursively sorted OrderedDict (by key).
    :param d: A dictionary to sort.
    :return: An OrderedDict.
    """
    res = OrderedDict()
    for k, v in sorted(d.items()):
        if isinstance(v, dict):
            res[k] = sort_dict(v)
        else:
            res[k] = v
    return res
