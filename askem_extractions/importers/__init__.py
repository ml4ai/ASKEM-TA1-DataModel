
from itertools import tee, filterfalse

def partition(pred, iterable):
    "Use a predicate to partition entries into false entries and true entries"
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return list(filter(pred, t2)), list(filterfalse(pred, t1))

from .arizona import import_arizona
from .mit import import_mit


__all__ = ["import_arizona", "import_mit", "partition"]
