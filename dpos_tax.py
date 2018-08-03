from tax_db import TaxDB
import csv
import requests
import time
import datetime
from util.config import use_network

test_acct = "AMpPxXJZ7qdLbNUrVQV82ozDF2UZgHGB5L"
atomic = 100000000
tax_rate = 0.24
year = 86400 * 365


def get_market_price(ts):
    url = 'https://min-api.cryptocompare.com/data/pricehistorical'
    fsym = 'ARK'
    tsyms = 'USD'
    adj_ts = ts+n['epoch']

    # set request params
    params = {"fsym": fsym,
              "tsyms": tsyms,
              "ts": adj_ts}

    r = requests.get(url, params=params)
    time.sleep(0.25)
    return r.json()['ARK']['USD']


def buy(acct):
    s = "buy"
    buys = taxdb.get_transactions(acct, s)
    buy_orders = create_buy_records(buys)

    return buy_orders


def create_buy_records(b):
    orders = []

    for counter, i in enumerate(b):

        # add attributes timestamp, total amount, tax lot
        ts = i[0]
        # don't include fee in incoming records
        order_amt = i[1] / atomic
        tax_lot = counter
        price = get_market_price(ts)
        market_value = price * order_amt
        convert_ts = convert_timestamp((ts+n['epoch']))
        withold = market_value * tax_rate

        # create order record including
        t = [tax_lot, ts, order_amt, price, market_value, withold, convert_ts, "open"]

        # append to buy_orders
        orders.append(t)

    return orders


def sell(acct):
    s = "sell"
    sells = taxdb.get_transactions(acct, s)
    sell_orders = create_sell_records(sells)

    return sell_orders


def create_sell_records(s):
    sells = []
    for i in s:
        ts = i[0]
        # include fees
        sell_amt = (i[1]+i[2]) / atomic
        price = get_market_price(ts)
        market_value = price * sell_amt
        convert_ts = convert_timestamp((ts + n['epoch']))

        # create sell record including
        t = [ts, sell_amt, price, market_value, convert_ts, 0, 0]

        # append to buy_orders
        sells.append(t)

    return sells


def convert_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def lotting(b,s):
    # create new list for buys
    tmp = b[:]

    for i in s:
        # initialize cap gains
        short_cap_gain = 0
        long_cap_gain = 0
        sold_quantity = i[1]
        sold_price = i[2]

        for j in tmp:
            lot_quantity = j[2]
            # check if lot has been used up to skip and move to next lot
            if lot_quantity == 0:
                pass

            # check to see if another lot needs relief
            elif sold_quantity > lot_quantity:
                cap_gain = (sold_price - j[3]) * lot_quantity
                gain_type = gain_classification(i[0], j[1])
                if gain_type == "st":
                    short_cap_gain += cap_gain
                else:
                    long_cap_gain += cap_gain

                # update lot - zero out and status
                j[2] -= lot_quantity
                j[7] = "lot sold"

                # update remaining sell amount
                sold_quantity -= lot_quantity

            # this executes on the final lot to relieve for the sell
            else:
                cap_gain = (sold_price - j[3]) * sold_quantity

                gain_type = gain_classification(i[0], j[1])
                if gain_type == "st":
                    short_cap_gain += cap_gain
                else:
                    long_cap_gain += cap_gain

                # update lot and status
                j[2] -= sold_quantity
                j[7] = "lot partially sold"
                break

        # update capital gains for sell record
        i[5] += short_cap_gain
        i[6] += long_cap_gain


def gain_classification(sts, bts):
    if (sts - bts) >= year:
        gain = "lt"
    else:
        gain = "st"

    return gain


def write_csv(b,s):
    # buy file
    b_file = "buys.csv"
    with open(b_file, "w") as output:
        fieldnames = ['tax lot', 'timstamp', 'buy amount', 'price', 'market value', 'staking income tax', 'datetime', 'lot status']
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(fieldnames)
        writer.writerows(b)

    s_file = "sells.csv"
    with open(s_file, "w") as output:
        fieldnames = ['timestamp', 'sell amount', 'price', 'market value', 'datetime', 'st-gain', 'lt-gain']
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(fieldnames)
        writer.writerows(s)

if __name__ == '__main__':

    n = use_network("ark")
    taxdb = TaxDB(n['database'], 'username', n['dbpassword'])
    
    buys = buy(test_acct)
    sells = sell(test_acct)

    print("before lotting")
    for i in buys:
        print(i)

    for i in sells:
        print(i)

    lotting(buys, sells)

    print("after lotting")
    for i in buys:
        print(i)

    for i in sells:
        print(i)

    # output to buy and sell csv

    write_csv(buys, sells)