from datetime import datetime
from collections import namedtuple

OutputRow = namedtuple('OutputRow', ['date', 'details', 'amount', 'transactionType'])

def ResolveProcessor(headers):
    #crude but.. 
    if IndexOrNegativeOne(headers, 'Particulars') >= 0:
        return PrimaryAccountProcessor()

    if IndexOrNegativeOne(headers, 'PrincipalBalance') >= 0:
        return LoanAccountProcessor()

    if IndexOrNegativeOne(headers, 'ProcessedDate') >= 0:
        return CreditCardAccountProcessor()

    return None

def IndexOrNegativeOne(array, value): 
    try: 
        return array.index(value)
    except ValueError: 
        return -1


# processor for regular account export. Expecting columns: 
# Type,Details,Particulars,Code,Reference,Amount,Date,ForeignCurrencyAmount,ConversionCharge
class PrimaryAccountProcessor:
    def ToOutputRow(self, row):
        details = f'{row[1]} {row[2]} {row[3]} {row[4]}'
        if not details.strip():
            details = row[0]
        amount = float(row[5])
        transactionType = 'Credit' if amount > 0 else 'Debit'
        transdate = datetime.strptime(row[6],'%d/%m/%Y').date()
        return OutputRow(transdate, details, amount, transactionType)

# processor for loan account. Expecting columns:
# Date,Details,Amount,PrincipalBalance
class LoanAccountProcessor:
    def ToOutputRow(self, row):
        amount = float(row[2])
        transactionType = 'Credit' if amount > 0 else 'Debit'
        transdate = datetime.strptime(row[0],'%d/%m/%Y').date()
        return OutputRow(transdate, row[1], amount, transactionType)

# processor for credit card account export. Flips Debit amounts to negative values. 
# Expecting columns: 
# Card,Type,Amount,Details,TransactionDate,ProcessedDate,ForeignCurrencyAmount,ConversionCharge
class CreditCardAccountProcessor:
    def ToOutputRow(self, row):
        transactionType = 'Credit' if row[1] == 'C' else 'Debit'
        amount = float(row[2])
        if (transactionType == 'Debit'):
            amount *= -1

        transdate = datetime.strptime(row[4],'%d/%m/%Y').date()
        return OutputRow(transdate, row[3], amount, transactionType)