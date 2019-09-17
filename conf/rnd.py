import numpy as np
import numpy.random as nr
from dateutil.relativedelta import relativedelta
from scipy.stats import truncnorm

seed = nr.RandomState(0)


def get_truncated(lower, upper, mu, sigma):
    return truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)


def gen_birth(contract):
    # Borrower has to be at least 25 at contract time, and not over 80 at contract end
    # Hence, limiting age between 26 and 74 years old (9515, 27085 days)
    return contract - relativedelta(days=nr.randint(9515, 27085))


def gen_amortization(birth, contract):
    # Amortization is conditional on age and contract date
    amortization = nr.randint(60, 360)
    # Checking to see if oldest borrower at the end of contract is above age limit of 80 years old
    while (birth + relativedelta(years=80) < contract + relativedelta(months=amortization)) is True:
        amortization = nr.randint(60, 360)
        print('stuck', birth, contract, amortization)
    return amortization


def get_new_values(contract):
    purchase_price = seed.randint(100000, 1200000)
    loan_amount = int((purchase_price * seed.uniform(.1, .7)))
    downpayment = purchase_price - loan_amount

    # Macroeconomics
    inflation = np.round(seed.normal(loc=.025, scale=.015), decimals=4)
    return_on_cash = np.round(inflation + get_truncated(0, .02, .02, .5).rvs(), decimals=4)
    interest_rate = np.round(seed.normal(loc=.06, scale=.02), 4)
    real_return = np.round((return_on_cash - inflation) * (1 - .15), 4)

    birth1 = gen_birth(contract)
    birth2 = gen_birth(contract)

    amortization_months = gen_amortization(min(birth1, birth2), contract)

    perc_borrower1 = np.round(seed.random_sample(), 2)
    perc_borrower2 = np.round(1 - perc_borrower1, 2)

    # Rental
    rent_percentage = np.round(get_truncated(0.02, .06, .03, .2).rvs(), 3)

    return [purchase_price, downpayment, loan_amount, inflation, return_on_cash, interest_rate, real_return,
            birth1, birth2,
            perc_borrower1, perc_borrower2, rent_percentage, amortization_months]
