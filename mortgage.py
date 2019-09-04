"""
The foundations of the code comes from:
https://github.com/jbmohler/mortgage/blob/master/mortgage.py
Authored by: Joel B. Mohler
However, function have been changed to fit the Brazilian SAC and PRICE mortgage systems of amortization
Bernardo A Furtado

"""
import argparse
from itertools import islice
import datetime

from numpy import pmt

MONTHS_IN_YEAR = 12


class Mortgage:
    def __init__(self, interest, months, amount, choice='sac'):
        self._interest = interest
        self._months = months
        self._amount = amount
        self._choice = choice.lower()

    def rate(self):
        return self._interest

    def monthly_rate(self):
        return (1 + self.rate()) ** (1 / MONTHS_IN_YEAR) - 1

    def month_growth(self):
        return 1 + self._interest / MONTHS_IN_YEAR

    def apy(self):
        return self.month_growth() ** MONTHS_IN_YEAR - 1

    def loan_years(self):
        return float(self._months) / MONTHS_IN_YEAR

    def loan_months(self):
        return self._months

    def amount(self):
        return self._amount

    def monthly_payment(self):
        interest = float(self.amount()) * self.monthly_rate()
        if self._choice == 'price':
            return pmt(self.monthly_rate(), self.loan_months(), -self.amount())
        else:
            amortization = float(self.amount()) / self.loan_months()
            return interest + amortization

    def annual_payment(self):
        return self.monthly_payment() * MONTHS_IN_YEAR

    def total_payout(self):
        if self._choice == 'price':
            return self.monthly_payment() * self.loan_months()
        else:
            return sum(month[0] + month[1]
                       for month in islice(self.monthly_payment_schedule(),
                                           int(self.loan_months())))

    def monthly_payment_schedule(self):
        monthly = self.monthly_payment()
        balance = self.amount()
        while True:
            interest = balance * self.monthly_rate()
            if monthly >= balance + interest:
                yield balance, interest
                break
            if self._choice == 'price':
                principle = monthly - interest
            else:
                principle = self.amount() / self.loan_months()
            yield principle, interest
            balance -= principle


def print_summary(m):
    print('{}:  {:.2f}'.format('Rate', m.rate()))
    print('{}:  {:.2f}'.format('Month Growth', m.month_growth()))
    print('{}:  {:.2f}'.format('APY', m.apy()))
    print('{}:  {:.2f}'.format('Payoff Years', m.loan_years()))
    print('{}:  {:.2f}'.format('Payoff Months', m.loan_months()))
    print('{}:  {:.2f}'.format('Amount', m.amount()))
    print('{}:  {:.2f}'.format('Monthly Payment', m.monthly_payment()))
    print('{}:  {:.2f}'.format('Annual Payment', m.annual_payment()))
    print('{}:  {:.2f}'.format('Total Payout', m.total_payout()))


def main():
    parser = argparse.ArgumentParser(description='Mortgage Amortization Tools')
    parser.add_argument('-i', '--interest', default=9.4, dest='interest')
    parser.add_argument('-y', '--loan-years', default=20, dest='years')
    parser.add_argument('-m', '--loan-months', default=None, dest='months')
    parser.add_argument('-a', '--amount', default=450000, dest='amount')
    args = parser.parse_args()

    if args.months:
        m = Mortgage(float(args.interest) / 100, float(args.months), args.amount)
    else:
        m = Mortgage(float(args.interest) / 100, float(args.years) * MONTHS_IN_YEAR, args.amount)

    print_summary(m)


if __name__ == '__main__':
    main()
