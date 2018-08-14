#!/usr/bin/env python
from core.psql import DB
from core.taxdb import TaxDB
from core.price import Price
from util.config import use_network
import time


day = 86400

def get_offset(e):
    offset = 0
    while ((e+offset) % day) != 0:
        offset += 1

    return (e+offset)


def get_timestamps(first, ts):
    l = []

    while first <= ts:
        l.append(first)
        first += day

    return l

if __name__ == '__main__':
    n = use_network("ark")
    psql = DB(n['database'], n['dbuser'], n['dbpassword'])
    taxdb = TaxDB(n['dbuser'])

    #get delegates and prices
    d = psql.get_delegates()
    p = Price()
    t = int(time.time())

    price = [p.get_market_price(t)]
    addresses = [i[0] for i in d]

    taxdb.update_prices(price)
    taxdb.update_delegates(addresses)













