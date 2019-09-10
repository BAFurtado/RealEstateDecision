import matplotlib.pyplot as plt
import pandas as pd

import comparisons

values = [.75, .9, 1, 1.1, 1.25]
# values = [1]


def overriding(ax):
    for each in values:
        save = comparisons.p.purchase_price, comparisons.p.rent
        comparisons.p.purchase_price *= each
        comparisons.p.rent *= each
        comparisons.main()
        comparisons.p.purchase_price, comparisons.p.rent = save
        plot(ax)


def plot(ax):
    data = pd.read_csv(comparisons.p.data, sep=';')
    # ax.plot(data['home_value'], label='Home value')
    # ax.plot(data['balance'], label='Debt')
    # ax.plot(data['equity'], label='Equity', color='red')
    ax.plot(data['rent_savings'], label="Savings when renting", color='green')
    ax.plot(data['purchase_savings'], label='Benefit of buying', color='blue')


def plotting():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Plotting time series
    overriding(ax)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend([handles[0], handles[1]], [labels[0], labels[1]], loc='best', frameon=False)
    ax.set(xlabel='Months', ylabel='Values', title='Comparison Rental x Ownership')
    # Include parameters used
    # plt.annotate('House price {:,.0f}, \ndownpayment {:,.0f}, \ninterest annual {:.3f}, years {:.0f}, '
    #              '\naluguel {:,.0f}, \ncash return annual {:.3f}, \ninflation {:.3f},'
    #              '\ntabela: {} \nhouse appreciation {:.3f}'.format(p.purchase_price, p.downpayment, p.interest_rate,
    #                                                                p.amortization_years,
    #                                                                p.rent, p.return_on_cash, p.inflation,
    #                                                                p.mortgage_choice,
    #                                                                p.real_return),
    #              fontsize=9, xy=(0.05, 0.67), xycoords='axes fraction', alpha=.5)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.yaxis.set_major_formatter(plt.FuncFormatter('${:,.0f}'.format))

    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    plt.savefig('res1.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    # comparisons.main()
    plotting()
