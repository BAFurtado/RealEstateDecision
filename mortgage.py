"""
The foundations of this module code comes from:
https://github.com/jbmohler/mortgage/blob/master/mortgage.py
Authored by: Joel B. Mohler
However, function have been changed to fit the Brazilian SAC and PRICE mortgage systems of amortization
Bernardo A Furtado

"""
import argparse
from itertools import islice

from numpy import pmt

MONTHS_IN_YEAR = 12


class Mortgage:
    def __init__(self, interest, months, amount, correction, choice='sac'):
        self._interest = interest
        self._months = months
        self._amount = amount
        self._correction = correction
        self._choice = choice.lower()

    def rate(self):
        return self._interest

    def monthly_rate(self):
        return (1 + self.rate()) ** (1 / MONTHS_IN_YEAR) - 1

    def monthly_correction(self):
        return (1 + self._correction) ** (1 / MONTHS_IN_YEAR) - 1

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

    def monetary_correction(self):
        self._amount *= (1 + self.monthly_correction())

    def get_monetary_correction(self):
        return self._amount * self.monthly_correction()

    def total_payout(self):
        return sum(month[0] + month[1]
                   for month in islice(self.monthly_payment_schedule(), int(self.loan_months())))

    def monthly_payment_schedule(self):
        for i in range(self.loan_months()):
            self.monetary_correction()
            interest = self._amount * self.monthly_rate()
            if self._choice == 'price':
                principle = pmt(self.monthly_rate(), self.loan_months() - i, -self.amount(), when=1) - interest
            else:
                principle = self._amount / (self.loan_months() - i)
            yield principle, interest
            self._amount -= principle


def print_summary(m):
    print('{}:  {:.2f}'.format('Rate', m.rate()))
    print('{}:  {:.2f}'.format('Month Growth', m.month_growth()))
    print('{}:  {:.2f}'.format('APY', m.apy()))
    print('{}:  {:.2f}'.format('Payoff Years', m.loan_years()))
    print('{}:  {:.2f}'.format('Payoff Months', m.loan_months()))
    print('{}:  {:.2f}'.format('Amount', m.amount()))
    print('{}:  {:.2f}'.format('Total Payout', m.total_payout()))


def main():
    parser = argparse.ArgumentParser(description='Mortgage Amortization Tools')
    parser.add_argument('-i', '--interest', default=9.4, dest='interest')
    parser.add_argument('-y', '--loan-years', default=20, dest='years')
    parser.add_argument('-m', '--loan-months', default=None, dest='months')
    parser.add_argument('-c', '--correction', default=0.01, dest='correction')
    parser.add_argument('-a', '--amount', default=450000, dest='amount')
    args = parser.parse_args()

    if args.months:
        m = Mortgage(float(args.interest) / 100, float(args.months), args.amount, args.correction)
    else:
        m = Mortgage(float(args.interest) / 100, float(args.years) * MONTHS_IN_YEAR, args.amount, args.correction)

    print_summary(m)


if __name__ == '__main__':
    main()
