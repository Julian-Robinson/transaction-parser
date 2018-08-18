import unittest
import rowhandlers


class Test_RowHandlers(unittest.TestCase):
    def test_PrimaryProcessor_MapsFieldsToOutputRow(self):
        # Type,Details,Particulars,Code,Reference,Amount,Date,ForeignCurrencyAmount,ConversionCharge
        row = ['Direct Credit','Details','Particulars','Code','Reference','-100.20','06/08/2018','','']
        sut = rowhandlers.PrimaryAccountProcessor()
        result = sut.ToOutputRow(row)

        self.assertEqual(result.date.isoformat(), '2018-08-06')
        self.assertEqual(result.amount, -100.20)
        self.assertEqual(result.transactionType, 'Debit')
        self.assertEqual(result.details, 'Details Particulars Code Reference')

        
    def test_CreditProcessor_MapsFieldsToOutputRow(self):
        # Card,Type,Amount,Details,TransactionDate,ProcessedDate,ForeignCurrencyAmount,ConversionCharge
        row = ['','C','20.50','Details','16/08/2018','16/08/2018','','']
        sut = rowhandlers.CreditCardAccountProcessor()
        result = sut.ToOutputRow(row)

        self.assertEqual(result.date.isoformat(), '2018-08-16')
        self.assertEqual(result.amount, 20.50)
        self.assertEqual(result.transactionType, 'Credit')
        self.assertEqual(result.details, 'Details')

    def test_CreditProcessor_FlipsDebitAmountsToNegativeValues(self):
        # Card,Type,Amount,Details,TransactionDate,ProcessedDate,ForeignCurrencyAmount,ConversionCharge
        row = ['','D','20.50','Details','16/08/2018','16/08/2018','','']
        sut = rowhandlers.CreditCardAccountProcessor()
        result = sut.ToOutputRow(row)

        self.assertEqual(result.amount, -20.50)
        self.assertEqual(result.transactionType, 'Debit')
        
    def test_LoanProcessor_MapsFieldsToOutputRow(self):
        # Date,Details,Amount,PrincipalBalance
        row = ['14/08/2018','Loan Payment','150.25','100']
        sut = rowhandlers.LoanAccountProcessor()
        result = sut.ToOutputRow(row)

        self.assertEqual(result.date.isoformat(), '2018-08-14')
        self.assertEqual(result.amount, 150.25)
        self.assertEqual(result.transactionType, 'Credit')
        self.assertEqual(result.details, 'Loan Payment')

if __name__ == '__main__':
    unittest.main()