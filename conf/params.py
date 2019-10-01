import datetime

# Purchasing
PURCHASE_PRICE = 400000
DOWNPAYMENT = 120000
LOAN_AMOUNT = PURCHASE_PRICE - DOWNPAYMENT
HOUSE_APPRECIATION = .05

FINANCING_RATE = .07

# Alternatives: 'price', 'sac'
MORTGAGE_CHOICE = 'sac'
SELLING_COST = .06
CONTRACT_DATE = datetime.date(2019, 9, 17)

# Borrowers' age (mutuários)
BIRTH1 = datetime.date(1980, 3, 28)
BIRTH2 = datetime.date(1977, 9, 1)

PERC_BORROWER1 = 1
PERC_BORROWER2 = 1 - PERC_BORROWER1

# Macroeconomics
INFLATION = .0375
TREASURE_RETURN = .0512

# Adjustment fees
# If correction includes inflation, add below
REFERENCIAL_FEE = 0
# REFERENCIAL_FEE = INFLATION

# Rental -- about 3.5% of home value per year
RENT_PERCENTAGE = .0029
RENT_RAISING_PERIOD = 12

AMORTIZATION_MONTHS = 240

TAX = .15
CUSTODY_FEE = .0003

# REAL
REAL_RETURN = round((TREASURE_RETURN - INFLATION) * (1 - TAX), 6)
REAL_HOUSE_APPRECIATION = round((HOUSE_APPRECIATION - INFLATION), 6)

# To save, give data a path and a name
# DATA = None
DATA = 'data.csv'
