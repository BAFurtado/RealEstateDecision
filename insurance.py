import datetime
import pandas as pd

# MIP applies to balance
# fee depends on ages and percentage of estate ownership

# DFI applies to a fixed fee on total value of estate

# Data
DFI = 7.8e-05
fees = pd.read_csv('fees.csv', sep=';') / 100


def age(d1, d2):
    return d1.year - d2.year - ((d1.month, d1.day) < (d2.month, d2.day))


def find_row(y):
    for i in range(len(fees.columns)):
        if str(y) < fees.columns[i]:
            return i


def fee(birth, contract, current):
    return fees.iloc[find_row(age(contract, birth)), find_row(age(current, birth))]


def mip(balance, contract_date, birth1, current_date=None, birth2=None, pc1=1., pc2=0.):
    return balance * fee(birth1, contract_date, current_date) * pc1 \
           + balance * fee(birth2, contract_date, current_date) * pc2


if __name__ == '__main__':
    original_value = 1038000
    bal = 157565.05
    contr = datetime.date(2013, 10, 23)
    b1 = datetime.date(1971, 10, 16)
    b2 = datetime.date(1966, 10, 16)
    cur_age = datetime.date(2019, 9, 4)
    # print(fee(b1, contr, cur_age))
    # print(fee(b2, contr, cur_age))
    p1 = .8601
    p2 = .1399
    m = mip(bal, contr, b1, datetime.date(2019, 9, 4), b2, p1, p2)
    d = dfi(original_value)
    print('MIP: {:,.2f}, DIF: {:,.2f} insurance: {:,.2f}'.format(m, d, m + d))

