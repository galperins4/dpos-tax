from tax_db import TaxDB
import requests
import time
import datetime


taxdb = TaxDB('ark_mainnet', 'username', 'password')

test_acct = "AMpPxXJZ7qdLbNUrVQV82ozDF2UZgHGB5L"
epoch = 1490119200
atomic = 100000000
tax_rate = 0.24

def get_market_price(ts):
    url = 'https://min-api.cryptocompare.com/data/pricehistorical'
    fsym = 'ARK'
    tsyms = 'USD'
    adj_ts = ts+epoch

    # set request params
    params = {"fsym": fsym,
              "tsyms": tsyms,
              "ts": adj_ts}

    r = requests.get(url, params=params)
    time.sleep(0.25)
    return r.json()['ARK']['USD']

def create_buy_records(b):
    orders = []
    counter = 1

    for i in b:
        # add attributes timestamp, total amount, tax lot
        ts = i[0]
        # don't include fee in incoming records
        order_amt = i[1] / atomic
        tax_lot = counter
        price = get_market_price(ts)
        market_value = price * order_amt
        convert_ts = convert_timestamp((ts+epoch))
        withold = market_value * tax_rate

        # create order record including
        t = [tax_lot, ts, order_amt, price, market_value, withold, convert_ts]

        # append to buy_orders
        orders.append(t)

        # increment counter
        counter += 1

    return orders

def buy(acct):

    s = "buy"
    buys = taxdb.get_transactions(acct, s)
    buy_orders = create_buy_records(buys)

    return buy_orders

def sell(acct):
    s = "sell"
    return taxdb.get_transactions(acct, s)

def convert_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    buys = buy(test_acct)
    sells = sell(test_acct)

    for i in buys:
        print(i)
