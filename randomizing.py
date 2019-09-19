from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import register_matplotlib_converters

import conf
import generalization
import plotting


KEYS = ['PURCHASE_PRICE', 'DOWNPAYMENT', 'LOAN_AMOUNT',
        'INFLATION', 'TREASURE_RETURN', 'FINANCING_RATE', 'REAL_RETURN',
        'BIRTH1', 'BIRTH2',
        'HOUSE_APPRECIATION', 'REAL_HOUSE_APPRECIATION',
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


def plot_hist(out):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rent = [o for o in out if o >= 0]
    buy = [o for o in out if o < 0]
    ax.hist(rent, bins=50, color='green', label='Rent')
    ax.hist(buy, bins=50, color='red', label='Buy')
    ax = plotting.basic_plot_config(ax)
    ax.xaxis.set_major_formatter(plt.FuncFormatter('${:,.0f}'.format))
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    plt.savefig('randomization', bbox_inches='tight')
    plt.show()


def main(size):
    register_matplotlib_converters()
    l0 = creating_params(size)
    # plot_params(l0)
    out = generalization.runs(l0)
    print(out)
    np.save('output_randomization', out)
    plot_hist(out)


if __name__ == '__main__':
    s = 1000
    main(s)
