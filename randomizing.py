from collections import defaultdict

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
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


def plot_bundled(list_dict):
    joined_params = defaultdict(list)
    for each in list_dict:
        for key in each.keys():
            joined_params[key].append(each[key])
    for k in joined_params.keys():
        fig, ax = plt.subplots()
        if 'BIRTH' in k:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.hist(joined_params[k], bins=50)
        ax.set_title(k)
        plt.savefig('params_variation/{}.png'.format(k))
        plt.savefig('params_variation/{}.pdf'.format(k), format='pdf', transparent=True)
        # plt.show()
    fig, axs = plt.subplots(5, 3, squeeze=False, figsize=(20, 15))
    plt.locator_params(nbins=3)
    for i, ks in enumerate(joined_params.keys()):
        axs[i % 5, i % 3].hist(joined_params[ks], bins=50)
        axs[i % 5, i % 3].set_title(ks, fontsize=7)
        if 'BIRTH' in ks:
            axs[i % 5, i % 3].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.savefig('params_variation/{}.png'.format('Parameters variation'))
    plt.savefig('params_variation/{}.pdf'.format('Parameters variation'), format='pdf', transparent=True)
    # plt.show()


def plot_hist(out):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Pìcking different colors for the results
    rent = [o for o in out if o >= 0]
    buy = [o for o in out if o < 0]

    # Make bins' sizes more adequate
    # TODO
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
    plt.savefig('randomization.png', bbox_inches='tight')
    plt.savefig('randomization.pdf', format='pdf', transparent=True, bbox_inches='tight')
    plt.show()


def main(size):
    register_matplotlib_converters()
    l0 = creating_params(size)
    plot_bundled(l0)
    out = generalization.runs(l0)
    print(out)
    np.save('output_randomization', out)
    plot_hist(out)
    percentage = len([i for i in out if i > 0])
    print('Renting is a better option in {:.2f}% of the {} cases simulated'.format(percentage, size))


if __name__ == '__main__':
    s = 20000
    main(s)
