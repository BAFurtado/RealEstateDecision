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
    count = 0
    while (birth + relativedelta(years=79) < contract + relativedelta(months=amortization)) is True:
        amortization = nr.randint(60, 360)
        count += 1
        if count > 360:
            amortization = 60
            break
    return amortization


def get_new_values(contract):
    purchase_price = seed.randint(100000, 1800000)
    loan_amount = int((purchase_price * seed.uniform(.1, .8)))
    downpayment = purchase_price - loan_amount

    # Macroeconomics
    inflation = np.round(seed.normal(loc=.04, scale=.025), decimals=6)
    # treasure_return = np.round(seed.normal(loc=.06, scale=.025), decimals=6)
    treasure_return = np.round(get_truncated(0, .06, .02, .5).rvs(), decimals=6)
    house_appreciation = np.round(seed.normal(loc=.02, scale=.05), decimals=6)
    # house_appreciation = np.round(get_truncated(0, .06, .02, .5).rvs(), decimals=6)
    financing_rate = np.round(seed.normal(loc=.08, scale=.05), 6)
    real_return = np.round((treasure_return - inflation) * (1 - .15), 6)
    real_house_return = np.round((house_appreciation - inflation) * (1 - .15), 6)
    # Rental
    rent_percentage = np.round(get_truncated(.0, .01, .0029, .5).rvs(), 6)

    birth1 = gen_birth(contract)
    birth2 = gen_birth(contract)
    perc_borrower1 = np.round(seed.random_sample(), 2)
    perc_borrower2 = np.round(1 - perc_borrower1, 2)

    amortization_months = gen_amortization(min(birth1, birth2), contract)

    return [purchase_price, downpayment, loan_amount, inflation, treasure_return, financing_rate, real_return,
            birth1, birth2, house_appreciation, real_house_return,
            perc_borrower1, perc_borrower2, rent_percentage, amortization_months]
