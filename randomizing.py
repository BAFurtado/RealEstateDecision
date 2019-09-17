import matplotlib.pyplot as plt

import conf
import generalization

KEYS = ['PURCHASE_PRICE', 'DOWNPAYMENT', 'LOAN_AMOUNT', 'INFLATION', 'RETURN_ON_CASH', 'INTEREST_RATE', 'REAL_RETURN',
        'BIRTH1', 'BIRTH2',
        'PERC_BORROWER1', 'PERC_BORROWER2', 'RENT_PERCENTAGE', 'AMORTIZATION_MONTHS']


def creating_params(size):
    lst = list()
    for i in range(size):
        ds = dict()
        values = conf.rnd.get_new_values(conf.PARAMS['CONTRACT_DATE'])
        for j, key in enumerate(KEYS):
            ds[key] = values[j]
        lst.append(ds)
    return lst


if __name__ == '__main__':
    s = 120
    l0 = creating_params(s)
    out = generalization.runs(l0)
    print(out)
    plt.hist(out, bins=50)
