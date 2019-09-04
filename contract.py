import datetime
from mortgage import Mortgage
import parameters as p


class Borrower:
    def __init__(self, birth):
        self.birth = birth


class Contract:
    def __init__(self, signature, value):
        self.signature = signature
        self.value = value
        self.borrowers = dict()

    def set_borrowers(self, b, percentage):
        self.borrowers[b] = percentage

    def set_mortgage(self, interest, months, loan, choice):
        self.mortage = Mortgage(interest, months, loan, choice)

    def output(self):
        pass


if __name__ == '__main__':
    original_value = 1038000
    b1 = Borrower(datetime.date(1971, 10, 16))
    b2 = Borrower(datetime.date(1966, 10, 16))
    c = Contract(datetime.date(2013, 10, 23), original_value)
    c.set_borrowers(b1, .8601)
    c.set_borrowers(b2, .1399)
    c.set_mortgage(p.interest_rate, p.amortization_months, p.loan_amount, p.mortgage_choice)

    # cur_age = datetime.date(2019, 9, 4)
    #
    # m = mip(bal, contr, b1, datetime.date(2019, 9, 4), b2, p1, p2)
    # d = dfi(original_value)
    # print('MIP: {:,.2f}, DIF: {:,.2f} insurance: {:,.2f}'.format(m, d, m + d))