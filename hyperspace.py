import generalization
import conf
import matplotlib.pyplot as plt


def plotting(values, output):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for key in output.keys():
        ax.plot(values, output[key], label='{}: {}'.format(key, conf.PARAMS[key]), alpha=.9, lw=.8)

    ax.legend(frameon=False, loc='best')
    ax.set(xlabel='Parameter Percentage Variation', ylabel='Present Value $ (negative: BUY)',
           title='Comparison Rental x Ownership')
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
    a = 'RENT_PERCENTAGE'
    b = 'INFLATION'
    c = 'LOAN_AMOUNT'
    # d = 'PURCHASE_PRICE'
    # e = 'DOWNPAYMENT'
    f = 'AMORTIZATION_MONTHS'
    g = 'INTEREST_RATE'
    print(a, conf.PARAMS[a])
    v, out = generalization.prepare(a, b, c, f, g)
    generalization.output(v, out)
    plotting(v, out)
