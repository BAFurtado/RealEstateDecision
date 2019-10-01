import copy

import numpy as np
from joblib import Parallel, delayed
from numpy import linspace, around

import comparisons


# o is a dictionary with overrides
def multiple(o, consistency):
    p = copy.deepcopy(comparisons.conf.PARAMS)
    if consistency:
        o = check_consistency(p, o)
    p.update(o)
    # print(p)
    return p


# Overrides are a list containing dictionaries. Each dictionary may contain one or more parameter changing
def runs(overrides, consistency=False):
    return Parallel(n_jobs=4)(delayed(comparisons.main)(multiple(o, consistency)) for o in overrides)


# Asserting that some values that are dependent on others are consistent!
def check_consistency(original, override):

    # If testing loan_amount, then purchase price varies accordingly, keeping downpayment fixed
    if 'LOAN_AMOUNT' in override.keys():
        override['PURCHASE_PRICE'] = original['DOWNPAYMENT'] + override['LOAN_AMOUNT']
    # If testing purchase_price, size of loan amount varies, keeping downpayment fixed
    if 'PURCHASE_PRICE' in override.keys():
        override['LOAN_AMOUNT'] = override['PURCHASE_PRICE'] - original['DOWNPAYMENT']
    # If testing downpayment, loan_amount will vary, keeping the original purchasing price
    if 'DOWNPAYMENT' in override.keys():
        override['LOAN_AMOUNT'] = original['PURCHASE_PRICE'] - override['DOWNPAYMENT']

    if 'AMORTIZATION_MONTHS' in override.keys():
        if override['AMORTIZATION_MONTHS'] < 60:
            override['AMORTIZATION_MONTHS'] = 60
        elif override['AMORTIZATION_MONTHS'] > 360:
            override['AMORTIZATION_MONTHS'] = 360

    # If testing inflation, both real return and house real appreciation will be affected
    if 'INFLATION' in override.keys():
        override['REAL_RETURN'] = np.round((original['TREASURE_RETURN'] - override['INFLATION'])
                                           * (1 - original['TAX']), 6)
        override['REAL_HOUSE_APPRECIATION'] = np.round((original['TREASURE_RETURN'] - override['INFLATION'])
                                                       * (1 - original['TAX']), 6)

    if 'TREASURE_RETURN' in override.keys():
        override['REAL_RETURN'] = np.round((override['TREASURE_RETURN'] - original['INFLATION'])
                                           * (1 - original['TAX']), 4)

    if 'TAX' in override.keys():
        override['REAL_RETURN'] = np.round((original['TREASURE_RETURN'] - original['INFLATION'])
                                           * (1 - override['TAX']), 4)
        override['REAL_HOUSE_APPRECIATION'] = np.round((original['TREASURE_RETURN'] - original['INFLATION'])
                                                       * (1 - override['TAX']), 4)

    if 'AMORTIZATION_MONTHS' in override.keys():
        override['AMORTIZATION_MONTHS'] = int(override['AMORTIZATION_MONTHS'])
    return override


def prepare(*parameter):
    output = dict()
    values = linspace(.25, 2, 8)
    for each in parameter:
        l0 = list()
        for v in values:
            l0.append({each: round(v * comparisons.conf.PARAMS[each], 4)})
        output[each] = runs(l0, True)
    return around(values, 4), output


def results(values, res):
    for key in res.keys():
        print(key)
        for i in range(len(values)):
            print(values[i], res[key][i])


if __name__ == '__main__':
    f = 'RENT_PERCENTAGE'
    d = 'REAL_HOUSE_APPRECIATION'
    e = 'REAL_RETURN'
    v, out = prepare(d, e, f)
    results(v, out)
