import copy

from joblib import Parallel, delayed
from numpy import linspace, around
import comparisons


# Overrides are a list containing dictionaries. Each dictionary may contain one or more parameter changing
def multiple(o):
    p = copy.deepcopy(comparisons.conf.PARAMS)
    p.update(o)
    return p


def runs(overrides):
    return Parallel(n_jobs=4)(delayed(comparisons.main)(multiple(o)) for o in overrides)


def prepare(*parameter):
    output = dict()
    values = linspace(.5, 1.5, 10)
    for each in parameter:
        d0 = list()
        for v in values:
            d0.append({each: round(v * comparisons.conf.PARAMS[each], 4)})
        output[each] = runs(d0)
    return around(values, 4), output


def output(values, res):
    for key in res.keys():
        print(key)
        for i in range(len(values)):
            print(values[i], res[key][i])


if __name__ == '__main__':
    a = 'RENT_PERCENTAGE'
    b = 'INFLATION'
    v, out = prepare(a, b)
    output(v, out)
