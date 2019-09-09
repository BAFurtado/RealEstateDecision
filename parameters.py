import datetime

# Purchasing
purchase_price = 500000
downpayment = 250000
loan_amount = purchase_price - downpayment
interest_rate = .08
amortization_years = 30
amortization_months = None
mortgage_choice = 'sac'
selling_cost = .06
contract_date = datetime.date(2010, 1, 1)

# Borrowers' age (mutuários)
birth1 = datetime.date(1970, 1, 1)
birth2 = datetime.date(1970, 1, 1)
perc_borrower1 = .6
perc_borrower2 = .4


# Macroeconomics
inflation = .02
return_on_cash = .04

# Rental
rent_percentage = .002
rent = purchase_price * rent_percentage
rent_raising_period = 12

# Calculated values
if not amortization_months:
    amortization_months = amortization_years * 12

tax = .15
custody_fee = .0003
real_return = (return_on_cash - inflation) * (1 - tax)

data = 'data.csv'
