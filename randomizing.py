import numpy.random as nr
from scipy.stats import truncnorm
import datetime
import numpy as np


seed = nr.RandomState(0)
size = 10


def get_truncated(lower, upper, mu, sigma):
    return truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)


def gen_birth():
    return np.array([(np.datetime64('1959-01-01') + seed.choice(13140)).astype(datetime.datetime)
                     for i in range(size * 2)])


PURCHASE_PRICE = seed.randint(100000, 2500000, size=size)
DOWNPAYMENT = PURCHASE_PRICE * seed.uniform(.1, .8, size=size)
LOAN_AMOUNT = PURCHASE_PRICE - DOWNPAYMENT

# Macroeconomics
INFLATION = seed.normal(loc=.025, scale=.015, size=size)
RETURN_ON_CASH = INFLATION + get_truncated(0, .8, .02, .5).rvs(size=size)
INTEREST_RATE = seed.normal(loc=.07, scale=.02, size=size)
MORTGAGE_CHOICE = 'sac'
SELLING_COST = .06
CONTRACT_DATE = datetime.date(2019, 9, 1)

PERC_BORROWER1 = seed.random_sample(size)
PERC_BORROWER2 = 1 - PERC_BORROWER1

# Rental
RENT_PERCENTAGE = get_truncated(0.2, .65, .03, .2).rvs(size=size)
RENT_RAISING_PERIOD = 12

AMORTIZATION_MONTHS = seed.randint(60, 420, size=size)

TAX = .15
CUSTODY_FEE = .0003

REAL_RETURN = round((RETURN_ON_CASH - INFLATION) * (1 - TAX), 4)

DATA = 'data.csv'

# Prepare a list of dictionaries, send them all off
