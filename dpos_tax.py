from tax_db import TaxDB

taxdb = TaxDB('db', 'username', 'db_pw')
test_acct = "AMpPxXJZ7qdLbNUrVQV82ozDF2UZgHGB5L"


def buy(acct):
    s = "buy"
    return taxdb.get_transactions(acct, s)

def sell(acct):
    s = "sell"
    return taxdb.get_transactions(acct, s)

if __name__ == '__main__':
    buys = buy(test_acct)
    sells = sell(test_acct)

    print("buys", buys)
    print("sells", sells)
