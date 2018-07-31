from tax_db import TaxDB

taxdb = TaxDB('db', 'username', 'db_pw')
test_acct = "AMpPxXJZ7qdLbNUrVQV82ozDF2UZgHGB5L"

buy(test_acct)

def buy(acct):
    s = "buy"
    testing = taxdb.get_transactions(acct, s)
    print(testing)

def sell(acct):
    s = "sell"


