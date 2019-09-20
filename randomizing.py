from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from matplotlib.patches import Patch
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
    ax.hist(rent, bins=30, color='green', alpha=.3)
    ax.hist(buy, bins=70, color='red', alpha=.3)
    ax = plotting.basic_plot_config(ax)
    # loc = plticker.MultipleLocator(base=1.5e6)  # this locator puts ticks at regular intervals
    # ax.xaxis.set_major_locator(loc)
    plt.locator_params(nbins=5)
    ax.xaxis.set_major_formatter(plt.FuncFormatter('${:,.0f}'.format))
    legend_elements = [Patch(facecolor='green', edgecolor='green', alpha=.3, label='Rent'),
                       Patch(facecolor='red', edgecolor='red', alpha=.3, label='Buy')]
    ax.legend(handles=legend_elements, frameon=False, loc='best', title='Optimal decision')
    plt.title('Histogram of comparison buy x rent with randomized parameters')
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    plt.tick_params(axis='both', which='both', bottom=True, top=False,
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
