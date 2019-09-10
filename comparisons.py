import pandas as pd
from dateutil.relativedelta import relativedelta

import insurance
import parameters as p
from mortgage import Mortgage, MONTHS_IN_YEAR
from numpy import pv


def monthly_rate(rate):
    return (1 + rate) ** (1 / MONTHS_IN_YEAR) - 1


class Comparison:
    def __init__(self):
        self.data = pd.DataFrame()

    def save(self):
        self.data.to_csv(p.data, sep=';', index=False)

    def investment_return(self, amount, months, rate, title='rent_savings'):
        for i in range(months):
            if i == 0:
                self.data.loc[0, title] = amount
            else:
                if title == 'rent_savings':
                    amount += self.save_rent_different(i)
                    if i % 12 == 0:
                        amount *= (1 - p.custody_fee)
                amount *= 1 + monthly_rate(rate)
                self.data.loc[i, title] = amount
        self.save()

    def save_rent_different(self, j):
        return self.data.loc[j, 'payment'] - self.data.loc[j, 'rent']

    def equity(self):
        self.data.loc[:, 'equity'] = self.data.loc[:, 'home_value'] - self.data.loc[:, 'balance']
        self.selling()
        self.save()

    def selling(self):
        self.data.loc[:, 'purchase_savings'] = self.data.loc[:, 'equity'] - \
                                               self.data.loc[:, 'home_value'] * p.selling_cost

    def present_value_buying(self):
        return pv(p.real_return / MONTHS_IN_YEAR,
                  p.amortization_months,
                  0,
                  self.data.loc[p.amortization_months - 1, 'purchase_savings'] -
                  self.data.loc[p.amortization_months - 1, 'rent_savings'])


class Rental:
    def __init__(self, base):
        self.data = base.data

    def gen_rent(self, rent, months, inflation, period_adjustment):
        for i in range(months):
            self.data.loc[i, 'rent'] = round(rent, 2)
            if (i % (period_adjustment - 1)) == 0 and i > 0:
                rent *= (1 + inflation)
        self.data.to_csv(p.data, sep=';', index=False)


class Borrower:
    def __init__(self, birth):
        self.birth = birth


class Contract:
    def __init__(self, signature, value, base):
        self.signature = signature
        self.value = value
        self.borrowers = dict()
        self.mortgage = None
        self.data = base.data

    def set_borrowers(self, b, percentage):
        self.borrowers[b] = percentage

    def set_mortgage(self, interest, months, loan, choice):
        self.mortgage = Mortgage(interest, months, loan, choice)

    def gen_schedule(self):
        for i, payment in enumerate(self.mortgage.monthly_payment_schedule()):
            self.data.loc[i, 'amortization'] = round(payment[0], 2)
            self.data.loc[i, 'interest'] = round(payment[1], 2)

    def complete_schedule(self):
        self.data.loc[0, 'balance'] = p.loan_amount - self.data.loc[0, 'amortization']
        for i in range(1, len(self.data)):
            self.data.loc[i, 'balance'] = self.data.loc[i - 1, 'balance'] - self.data.loc[i, 'amortization']
        self.data.loc[:, 'dfi'] = round(self.dfi(), 2)
        self.mip()
        self.data.loc[:, 'payment'] = self.data.amortization + self.data.interest \
                                               + self.data.dfi + self.data.mip
        self.data.to_csv(p.data, sep=';', index=False)

    def dfi(self):
        return self.value * insurance.DFI

    def mip(self):
        keys = list(self.borrowers.keys())
        for i in range(len(self.data)):
            self.data.to_csv(p.data, sep=';', index=False)
            self.data.loc[i, 'mip'] = insurance.mip(self.data.loc[i, 'balance'], self.signature,
                                                          keys[0].birth, self.signature + relativedelta(months=i),
                                                          keys[1].birth if keys[1] else None,
                                                          self.borrowers[keys[0]],
                                                          self.borrowers[keys[1]] if keys[1] else None)


def main():
    # Sequence of events
    # Initiate a comparison
    d = Comparison()

    # Import at most two borrowers with birthdate and percentage of ownership
    b1 = Borrower(p.birth1)
    b2 = Borrower(p.birth2)

    # Set the contract
    c = Contract(p.contract_date, p.purchase_price - p.downpayment, d)
    c.set_borrowers(b1, p.perc_borrower1)
    c.set_borrowers(b2, p.perc_borrower2)
    c.set_mortgage(p.interest_rate, p.amortization_months, p.loan_amount, p.mortgage_choice)

    # Run schedule generation
    c.gen_schedule()
    c.complete_schedule()

    # Include rental details and investments
    rental = Rental(d)
    rental.gen_rent(p.rent, p.amortization_months, p.inflation, p.rent_raising_period)
    # Investment return includes money saved from not making mortgage payments
    d.investment_return(p.downpayment, p.amortization_months, p.real_return, 'rent_savings')
    d.investment_return(p.purchase_price, p.amortization_months, p.real_return, 'home_value')
    d.equity()
    return d.present_value_buying()


if __name__ == '__main__':
    output = main()
    print(output)
