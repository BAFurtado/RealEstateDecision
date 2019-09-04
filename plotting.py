from mortgage import Mortgage
import parameters as p
from itertools import islice


if __name__ == '__main__':
    # Order of parameters: interest_rate, months, amount
    m = Mortgage(p.interest_rate, p.amortization_months, p.loan_amount)

    # Test for month 1
    print(m.monthly_payment('price'))
    print(type(m.monthly_payment()))

    # Print schedule: principle and interest
    # for index, payment in enumerate(m.monthly_payment_schedule()):
    #     print(payment)

    # Amount paid first 10 years
    # Principal
    print(sum(month[0] for month in islice(m.monthly_payment_schedule(), 120)))
    # Interest
    print(m.total_payout())

