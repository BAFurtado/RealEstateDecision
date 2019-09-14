import datetime

import numpy as np
import numpy.random as nr
from scipy.stats import truncnorm


def get_truncated(lower, upper, mu, sigma):
    return truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)


def gen_birth():
    return (np.datetime64('1959-01-01') + nr.choice(13140)).astype(datetime.datetime)


def get_new_values():
    PURCHASE_PRICE = nr.randint(100000, 1200000)
    DOWNPAYMENT = int((PURCHASE_PRICE * nr.uniform(.1, .7)))

    # Macroeconomics
    INFLATION = np.round(nr.normal(loc=.025, scale=.015), decimals=4)
    RETURN_ON_CASH = np.round(INFLATION + get_truncated(0, .02, .02, .5).rvs(), decimals=4)
    INTEREST_RATE = np.round(nr.normal(loc=.06, scale=.02), 4)

    BIRTH1 = gen_birth()
    BIRTH2 = gen_birth()

    PERC_BORROWER1 = np.round(nr.random_sample(), 2)
    PERC_BORROWER2 = np.round(1 - PERC_BORROWER1, 2)

    # Rental
    RENT_PERCENTAGE = np.round(get_truncated(0.02, .06, .03, .2).rvs(), 3)

    AMORTIZATION_MONTHS = nr.randint(60, 360)
    return [PURCHASE_PRICE, DOWNPAYMENT, INFLATION, RETURN_ON_CASH, INTEREST_RATE, BIRTH1, BIRTH2, PERC_BORROWER1,\
           PERC_BORROWER2, RENT_PERCENTAGE, AMORTIZATION_MONTHS]
