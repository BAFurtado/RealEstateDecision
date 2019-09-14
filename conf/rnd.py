import datetime

import numpy as np
import numpy.random as nr
from scipy.stats import truncnorm


def get_truncated(lower, upper, mu, sigma):
    return truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)


def gen_birth():
    return (np.datetime64('1959-01-01') + nr.choice(13140)).astype(datetime.datetime)


def get_new_values():
    purchase_price = nr.randint(100000, 1200000)
    loan_amount = int((purchase_price * nr.uniform(.1, .7)))
    downpayment = purchase_price - loan_amount

    # Macroeconomics
    inflation = np.round(nr.normal(loc=.025, scale=.015), decimals=4)
    return_on_cash = np.round(inflation + get_truncated(0, .02, .02, .5).rvs(), decimals=4)
    interest_rate = np.round(nr.normal(loc=.06, scale=.02), 4)
    real_return = np.round((return_on_cash - inflation) * (1 - .15), 4)

    birth1 = gen_birth()
    birth2 = gen_birth()

    perc_borrower1 = np.round(nr.random_sample(), 2)
    perc_borrower2 = np.round(1 - perc_borrower1, 2)

    # Rental
    rent_percentage = np.round(get_truncated(0.02, .06, .03, .2).rvs(), 3)

    amortization_months = nr.randint(60, 360)
    return [purchase_price, downpayment, loan_amount, inflation, return_on_cash, interest_rate, real_return,
            birth1, birth2,
            perc_borrower1, perc_borrower2, rent_percentage, amortization_months]
