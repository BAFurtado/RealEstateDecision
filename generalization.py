import copy

from joblib import Parallel, delayed
from numpy import linspace, around
import comparisons


# Overrides are a list containing dictionaries. Each dictionary may contain one or more parameter changing
def multiple(o):
    p = copy.deepcopy(comparisons.conf.PARAMS)
    o = check_consistency(p, o)
    print(o)
    p.update(o)
    return p


def runs(overrides):
    return Parallel(n_jobs=4)(delayed(comparisons.main)(multiple(o)) for o in overrides)


def check_consistency(original, override):
    if 'LOAN_AMOUNT' in override.keys():
        override['PURCHASE_PRICE'] = original['DOWNPAYMENT'] + override['LOAN_AMOUNT']
    if 'PURCHASE_PRICE' in override.keys():
        override['LOAN_AMOUNT'] = override['PURCHASE_PRICE'] - original['DOWNPAYMENT']
    if 'DOWNPAYMENT' in override.keys():
        override['LOAN_AMOUNT'] = original['PURCHASE_PRICE'] - override['DOWNPAYMENT']
    if 'INFLATION' in override.keys():
        temp = round((original['RETURN_ON_CASH'] - override['INFLATION'])
                                        * (1 - original['TAX']), 4)
        if temp == 0:
            override['REAL_RETURN'] = .00001
        else:
            override['REAL_RETURN'] = temp
    if 'RETURN_ON_CASH' in override.keys():
        override['REAL_RETURN'] = round((override['RETURN_ON_CASH'] - original['INFLATION'])
                                        * (1 - original['TAX']), 4)
    if 'TAX' in override.keys():
        override['REAL_RETURN'] = round((original['RETURN_ON_CASH'] - original['INFLATION'])
                                        * (1 - override['TAX']), 4)
    if 'REAL_RETURN' in override.keys():
        temp = round((override['REAL_RETURN'] + original['INFLATION'])
                                        / (1 - original['TAX']), 4)
        if temp == 0:
            override['RETURN_ON_CASH'] = .00001
        else:
            override['RETURN_ON_CASH'] = temp

    return override


def prepare(*parameter):
    output = dict()
    values = linspace(.5, 2, 4)
    for each in parameter:
        d0 = list()
        for v in values:
            d0.append({each: round(v * comparisons.conf.PARAMS[each], 4)})
        output[each] = runs(d0)
    return around(values, 4), output


def results(values, res):
    for key in res.keys():
        print(key)
        for i in range(len(values)):
            print(values[i], res[key][i])


if __name__ == '__main__':
    a = 'LOAN_AMOUNT'
    b = 'PURCHASE_PRICE'
    v, out = prepare(a, b)
    results(v, out)
