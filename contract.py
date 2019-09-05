import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

import insurance
import parameters as p
from mortgage import Mortgage


class Borrower:
    def __init__(self, birth):
        self.birth = birth


class Contract:
    def __init__(self, signature, value):
        self.signature = signature
        self.value = value
        self.borrowers = dict()
        self.mortgage = None
        self.data = pd.DataFrame()

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
        self.data.loc[:, 'total'] = self.data.amortization + self.data.interest + self.data.dfi + self.data.mip
        self.data.to_csv('data.csv', sep=';', index=False)

    def dfi(self):
        return self.value * insurance.DFI

    def mip(self):
        keys = list(self.borrowers.keys())
        for i in range(len(self.data)):
            self.data.loc[i, 'mip'] = round(insurance.mip(self.data.loc[i, 'balance'], self.signature,
                                                          keys[0].birth, self.signature + relativedelta(months=i),
                                                          keys[1].birth if keys[1] else None,
                                                          self.borrowers[keys[0]],
                                                          self.borrowers[keys[1]] if keys[1] else None), 2)


if __name__ == '__main__':
    original_value = 1038000
    b1 = Borrower(datetime.date(1971, 10, 16))
    b2 = Borrower(datetime.date(1966, 10, 16))
    c = Contract(datetime.date(2013, 10, 23), original_value)
    c.set_borrowers(b1, .8601)
    c.set_borrowers(b2, .1399)
    c.set_mortgage(p.interest_rate, p.amortization_months, p.loan_amount, p.mortgage_choice)
    c.gen_schedule()
    c.complete_schedule()
