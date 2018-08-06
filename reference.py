#!/usr/bin/env python
from core.psql import TaxDB
from util.config import use_network
import time
import requests

def get_market_price(ts):
    url = 'https://min-api.cryptocompare.com/data/pricehistorical'
    fsym = 'ARK'
    tsyms = 'USD,EUR'

    # set request params
    params = {"fsym": fsym,
              "tsyms": tsyms,
              "ts": ts}

    r = requests.get(url, params=params)

    output = [ts, r.json()['ARK']['USD'], r.json()['ARK']['EUR']]

    return output

if __name__ == '__main__':
    n = use_network("ark")
    psql = TaxDB(n['database'], n['dbuser'], n['dbpassword'])
    taxdb = TaxDB(n['dbuser'])

    #get delegates and prices
    d = psql.get_delegates()
    t = int(time.time())
    price = [get_market_price(t)]

    taxdb.update_prices(price)
    taxdb_update_delegates(d)













