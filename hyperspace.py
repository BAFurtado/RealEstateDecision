import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from numpy import arange

import conf
import generalization


def plotting(values, output):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for key in output.keys():
        ax.plot(values, output[key], label='{}: {}'.format(key, conf.PARAMS[key]), alpha=1, lw=1.1)

    x = arange(values.min(), values.max(), .01)
    ax.fill_between(x, max([max(i) for i in output.values()]), 0, where=max(max(output.values())) > 0,
                    facecolor='green', alpha=.3)
    ax.fill_between(x, 0, min([min(i) for i in output.values()]), where=min([min(i) for i in output.values()]) < 0,
                    facecolor='red', alpha=.3)

    handles, labels = ax.get_legend_handles_labels()
    legend_elements = [Patch(facecolor='green', edgecolor='green', alpha=.3, label='Rent'),
                       Patch(facecolor='red', edgecolor='red', alpha=.3, label='Buy')]
    ax.legend(handles=legend_elements + handles, frameon=False, loc="upper right",
              bbox_to_anchor=(1, 0, 0.5, 1), title='Parameter Value Reference')

    ax.set(xlabel='Multiplying Parameter Factor', ylabel='Present Value $',
           title='Comparison Rental x Ownership')

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.2f}x'.format))
    ax.yaxis.set_major_formatter(plt.FuncFormatter('${:,.0f}'.format))

    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    plt.savefig('res1.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    a = 'RENT_PERCENTAGE'
    b = 'INFLATION'
    c = 'LOAN_AMOUNT'
    d = 'PURCHASE_PRICE'
    e = 'DOWNPAYMENT'
    f = 'AMORTIZATION_MONTHS'
    g = 'INTEREST_RATE'
    h = 'REAL_RETURN'
    print(a, conf.PARAMS[a])
    v, out = generalization.prepare(b, h, e, f)
    generalization.results(v, out)
    plotting(v, out)
