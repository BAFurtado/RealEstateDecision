# Purchasing

purchase_price = 933000
downpayment = 483000
loan_amount = purchase_price - downpayment
interest_rate = .084
amortization_years = 20
amortization_months = None
mortgage_choice = 'sac'

selling_cost = .06

# Macroeconomics
inflation = .02
return_on_cash = .04

# Rental
rent_percentage = .003
rent = purchase_price * rent_percentage
rent_raising_period = 12

# Calculated values
if not amortization_months:
    amortization_months = amortization_years * 12

tax = .15
custody_fee = .0003
real_return = (return_on_cash - inflation) * (1 - tax)

data = 'data.csv'
