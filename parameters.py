appraisal_value = 1038000
purchase_price = 933000
downpayment = 483000
loan_amount = purchase_price - downpayment
interest_rate = .084
amortization_years = 240
amortization_months = None

mortgage_choice = 'sac'

appreciation = .03
inflation = .02
rent_raising_period = 12

cost_renting = 2500
return_on_cash = .04

# Calculated values
if not amortization_months:
    amortization_months = amortization_years * 12

real_return = return_on_cash - inflation
