from mortgage import Mortgage, print_summary
import parameters as p
from itertools import islice


if __name__ == '__main__':
    # Order of parameters: interest_rate, months, amount
    m = Mortgage(p.interest_rate, p.amortization_months, p.loan_amount, p.mortgage_choice)

    # Print schedule: principle and interest
    for payment in islice(m.monthly_payment_schedule(), 10):
        print('Princ. {:,.2f}, int. {:,.2f}, total: {:,.2f}'.format(payment[0], payment[1],
                                                                 payment[0] + payment[1]))

    # Amount paid first 10 years
    # Principal
    # print(sum(month[0] for month in islice(m.monthly_payment_schedule(), 240)))
    # # Total payment
    # print('{:,.2f}'.format(m.total_payout()))
    # print('')
    # print_summary(m)
