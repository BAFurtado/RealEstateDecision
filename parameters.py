purchase_price = 92000
downpayment = 0
interest_rate = .084
amortization_years = 20
amortization_months = 50

mortgage_choice = 'sac'

property_tax = 1
appreciation = 3
inflation = 2

cost_renting = 2500
return_on_cash = 6

# Calculated values
if not amortization_months:
    amortization_months = amortization_years * 12

loan_amount = purchase_price - downpayment
nominal_return_cash = return_on_cash - inflation
