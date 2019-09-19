from collections import defaultdict

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import conf
import generalization
import numpy as np

KEYS = ['PURCHASE_PRICE', 'DOWNPAYMENT', 'LOAN_AMOUNT', 'INFLATION', 'TREASURE_RETURN', 'FINANCING_RATE', 'REAL_RETURN',
        'BIRTH1', 'BIRTH2', 'HOUSE_APPRECIATION', 'REAL_HOUSE_APPRECIATION',
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


def plot_params(list_dict):
    joined_params = defaultdict(list)
    for each in list_dict:
        for key in each.keys():
            joined_params[key].append(each[key])
    for k in joined_params.keys():
        plt.hist(joined_params[k], bins=50)
        plt.title(k)
        plt.savefig('params_variation/{}.png'.format(k))
        plt.show()


if __name__ == '__main__':
    register_matplotlib_converters()
    s = 200
    l0 = creating_params(s)
    plot_params(l0)
    out = generalization.runs(l0)
    print(out)
    np.save('output_randomization', out)
    plt.hist(out, bins=50)
    plt.savefig('randomization.png')
    plt.show()
