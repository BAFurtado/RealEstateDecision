import pandas as pd
from dateutil.relativedelta import relativedelta
from numpy import pv

import conf
import insurance
from mortgage import Mortgage, MONTHS_IN_YEAR


def monthly_rate(rate):
    return (1 + rate) ** (1 / MONTHS_IN_YEAR) - 1


class Comparison:
    def __init__(self, p):
        self.data = pd.DataFrame()
        self.params = p

    def save(self):
        self.data.to_csv(self.params['DATA'], sep=';', index=False)
        # pass

    def investment_return(self, amount, months, rate, title='rent_savings'):
        for i in range(int(months)):
            if i == 0:
                self.data.loc[0, title] = amount
            else:
                if title == 'rent_savings':
                    # Increase the amount every month buy the difference between renting and paying mortgage
                    amount += self.save_rent_different(i)
                    # Discount annual administration fees
                    if i % 12 == 0:
                        amount *= (1 - self.params['CUSTODY_FEE'])
                # Either renting or paying mortgage there is a house appreciation or a capital return
                amount *= 1 + monthly_rate(rate)
                self.data.loc[i, title] = amount

    def save_rent_different(self, j):
        return self.data.loc[j, 'payment'] - self.data.loc[j, 'rent']

    def tax_capital_gains(self):
        # Taxes apply to the difference between downpayment plus full installment payments and original home value
        total_payment = sum(self.data.loc[:, 'payment']) + self.data.loc[0, 'rent_savings']
        if total_payment < self.data.loc[self.params['AMORTIZATION_MONTHS'] - 1, 'home_value']:
            return (self.data.loc[self.params['AMORTIZATION_MONTHS'] - 1, 'home_value'] - total_payment) \
                   * self.params['TAX']
        return 0

    def equity(self):
        self.data.loc[:, 'equity'] = self.data.loc[:, 'home_value'] - self.data.loc[:, 'balance']
        self.selling()
        self.save()

    def selling(self):
        self.data.loc[:, 'purchase_savings'] = self.data.loc[:, 'equity'] - \
                                               self.data.loc[:, 'home_value'] * self.params['SELLING_COST']

    def present_value_buying(self):
        return pv(self.params['REAL_RETURN'] / MONTHS_IN_YEAR,
                  self.params['AMORTIZATION_MONTHS'],
                  0,
                  self.data.loc[self.params['AMORTIZATION_MONTHS'] - 1, 'purchase_savings'] -
                  self.tax_capital_gains() -
                  self.data.loc[self.params['AMORTIZATION_MONTHS'] - 1, 'rent_savings'])


class Rental:
    def __init__(self, base):
        self.data = base.data
        self.params = base.params

    def gen_rent(self, rent, months, appreciation, period_adjustment):
        for i in range(int(months)):
            self.data.loc[i, 'rent'] = round(rent, 2)
            if (i % (period_adjustment - 1)) == 0 and i > 0:
                rent *= (1 + appreciation)


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
        self.params = base.params

    def set_borrowers(self, b, percentage):
        self.borrowers[b] = percentage

    def set_mortgage(self, interest, months, loan, correction, choice):
        self.mortgage = Mortgage(interest, months, loan, correction, choice)

    def gen_schedule(self):
        for i, payment in enumerate(self.mortgage.monthly_payment_schedule()):
            self.data.loc[i, 'correction'] = round(self.mortgage.get_monetary_correction(), 2)
            self.data.loc[i, 'amortization'] = round(payment[0], 2)
            self.data.loc[i, 'interest'] = round(payment[1], 2)
            self.data.loc[i, 'balance'] = round(self.mortgage.amount() - payment[0], 2)

    def complete_schedule(self):
        self.data.loc[:, 'dfi'] = round(self.dfi(), 2)
        self.mip()
        self.data.loc[:, 'payment'] = self.data.amortization + self.data.interest + self.data.dfi + self.data.mip
        # self.data.to_csv(self.params['DATA'], sep=';', index=False)

    def dfi(self):
        return self.value * insurance.DFI

    def mip(self):
        keys = list(self.borrowers.keys())
        for i in range(len(self.data)):
            # self.data.to_csv(self.params['DATA'], sep=';', index=False)
            self.data.loc[i, 'mip'] = insurance.mip(self.data.loc[i, 'balance'], self.signature,
                                                          keys[0].birth, self.signature + relativedelta(months=i),
                                                          keys[1].birth if keys[1] else None,
                                                          self.borrowers[keys[0]],
                                                          self.borrowers[keys[1]] if keys[1] else None)


def main(p):
    # Sequence of events
    # Initiate a comparison
    d = Comparison(p)

    # Import at most two borrowers with birthdate and percentage of ownership
    b1 = Borrower(p['BIRTH1'])
    b2 = Borrower(p['BIRTH2'])

    # Set the contract
    c = Contract(p['CONTRACT_DATE'], p['PURCHASE_PRICE'] - p['DOWNPAYMENT'], d)
    c.set_borrowers(b1, p['PERC_BORROWER1'])
    c.set_borrowers(b2, p['PERC_BORROWER2'])

    if p['MORTGAGE_CHOICE'] == 'sac_inflation':
        p['REFERENCIAL_FEE'] = p['INFLATION']

    c.set_mortgage(p['FINANCING_RATE'], p['AMORTIZATION_MONTHS'], p['LOAN_AMOUNT'], p['REFERENCIAL_FEE'],
                   p['MORTGAGE_CHOICE'])

    # Run schedule generation
    c.gen_schedule()
    c.complete_schedule()

    # Include rental details and investments
    rental = Rental(d)
    rental.gen_rent(p['PURCHASE_PRICE'] * p['RENT_PERCENTAGE'], p['AMORTIZATION_MONTHS'],
                    p['REAL_HOUSE_APPRECIATION'],
                    p['RENT_RAISING_PERIOD'])
    # Investment return includes money saved from not making mortgage payments
    d.investment_return(p['DOWNPAYMENT'], p['AMORTIZATION_MONTHS'], p['REAL_RETURN'],
                        'rent_savings')
    d.investment_return(p['PURCHASE_PRICE'], p['AMORTIZATION_MONTHS'], p['REAL_HOUSE_APPRECIATION'],
                        'home_value')
    d.equity()
    return round(d.present_value_buying(), 2)


if __name__ == '__main__':
    output = main(conf.PARAMS)
    print(output)
