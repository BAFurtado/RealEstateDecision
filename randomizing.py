import conf
import generalization
import copy
import importlib


KEYS = ['PURCHASE_PRICE', 'DOWNPAYMENT', 'INFLATION', 'RETURN_ON_CASH', 'INTEREST_RATE', 'BIRTH1', 'BIRTH2',
        'PERC_BORROWER1', 'PERC_BORROWER2', 'RENT_PERCENTAGE', 'AMORTIZATION_MONTHS']


def creating_params(size):
    lst = list()
    for i in range(size):
        ds = dict()
        values = conf.rnd.get_new_values()
        for j, key in enumerate(KEYS):
            ds[key] = values[j]
        lst.append(ds)
    return lst


if __name__ == '__main__':
    s = 10
    l0 = creating_params(s)
    for each in l0:
        for k in each.keys():
            print(k, each[k])
    out = generalization.runs(l0)
    print(out)
