import parameters as p


MONTHS_IN_YEAR = 12


def monthly_rate(rate):
    return (1 + rate) ** (1 / MONTHS_IN_YEAR) - 1


def spent_rent(rent, months, inflation, period_adjustment):
    spent = 0
    for i in range(months // period_adjustment):
        spent += rent * period_adjustment
        rent *= (1 + inflation)
    spent += rent * (months % period_adjustment)
    return round(spent, 2)


def cash_return(amount, months, rate):
    for i in range(months):
        amount *= (1 + monthly_rate(rate))
    return round(amount, 2)


if __name__ == '__main__':
    print(spent_rent(p.cost_renting, p.amortization_months, p.inflation, p.rent_raising_period))
    print(cash_return(p.downpayment, p.amortization_months, p.real_return))