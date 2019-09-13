import datetime

import numpy as np
import numpy.random as nr
from scipy.stats import truncnorm

seed = nr.RandomState(0)



def get_truncated(lower, upper, mu, sigma):
    return truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)


def gen_birth():
    return (np.datetime64('1959-01-01') + seed.choice(13140)).astype(datetime.datetime)


PURCHASE_PRICE = seed.randint(100000, 2500000)
DOWNPAYMENT = int((PURCHASE_PRICE * seed.uniform(.1, .8)))
LOAN_AMOUNT = PURCHASE_PRICE - DOWNPAYMENT

# Macroeconomics
INFLATION = np.round(seed.normal(loc=.025, scale=.015), decimals=4)
RETURN_ON_CASH = np.round(INFLATION + get_truncated(0, .08, .02, .5).rvs(), decimals=4)
INTEREST_RATE = np.round(seed.normal(loc=.07, scale=.02), 4)

SELLING_COST = .06
CONTRACT_DATE = datetime.date(2019, 9, 1)

BIRTH1 = gen_birth()
BIRTH2 = gen_birth()

PERC_BORROWER1 = np.round(seed.random_sample(), 2)
PERC_BORROWER2 = np.round(1 - PERC_BORROWER1, 2)

# Rental
RENT_PERCENTAGE = np.round(get_truncated(0.02, .065, .03, .2).rvs(), 3)
RENT_RAISING_PERIOD = 12

AMORTIZATION_MONTHS = seed.randint(60, 420)

TAX = .15
CUSTODY_FEE = .0003

REAL_RETURN = np.round((RETURN_ON_CASH - INFLATION) * (1 - TAX), 4)
