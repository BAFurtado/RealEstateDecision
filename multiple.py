import copy

from joblib import Parallel, delayed

import comparisons


# overrides are a list containing dictionaries. Each dictionary may contain one or more parameter changing
def multiple(o):
    p = copy.deepcopy(comparisons.conf.PARAMS)
    p.update(o)
    return p


def runs(overrides):
    res = Parallel(n_jobs=4)(delayed(comparisons.main)(multiple(o)) for o in overrides)
    print(res)


if __name__ == '__main__':
    rent_percentage = .002
    values = [.75, .9, 1, 1.1, 1.25]
    d0 = list()
    for v in values:
        d0.append({'RENT_PERCENTAGE': v * rent_percentage})
    runs(d0)
