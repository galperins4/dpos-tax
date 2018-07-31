from tax_db import TaxDB
import requests


taxdb = TaxDB('db', 'username', 'db_pw')

test_acct = "AMpPxXJZ7qdLbNUrVQV82ozDF2UZgHGB5L"
epoch = 1490101200
atomic = 100000000

def get_market_price(ts,v)
    url = 'https://min-api.cryptocompare.com/data/pricehistorical'
    fsym = 'ARK'
    tsyms = 'USD'

    adj_tx = ts+epoch

    # set request params
    params = {"fsym": fsym,
              "tsyms": tsyms,
              "ts": ts}

    r = requests.get(url, params=params)
    price = r.json()['ARK']['USD']
    tax_price = v * price

    return tax_price

def buy(acct):
    buy_orders = []
    counter = 1
    s = "buy"
    buys = taxdb.get_transactions(acct, s)

    for i in buys:
        # add attributes timestamp, total amount, tax lot
        ts = i[0]
        total_amt = (i[1]+i[2])/atomic
        tax_lot = counter
        market_value = get_market_price(ts, total_amt)

        # create order record including
        t = [ts, total_amt, tax_lot, total_amt, market_value]

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
