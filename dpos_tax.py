from tax_db import TaxDB

taxdb = TaxDB('db', 'username', 'db_pw')
test_acct = "AMpPxXJZ7qdLbNUrVQV82ozDF2UZgHGB5L"


def buy(acct):
    buy_orders = []
    counter = 1
    s = "buy"
    buys = taxdb.get_transactions(acct, s)

    for i in buys:
        # add attributes timestamp, total amount, tax lot
        ts = i[0]
        total_amt = i[1]+i[2]
        tax_lot = counter

        # create order record including
        t = [ts, total_amt, tax_lot, total_amt]

        # append to buy_orders
        buy_orders.append(t)

        # increment counter
        counter +=1

    return buy_orders

def sell(acct):
    s = "sell"
    return taxdb.get_transactions(acct, s)

if __name__ == '__main__':
    buys = buy(test_acct)
    sells = sell(test_acct)

    print("buys", buys)
    print("sells", sells)
