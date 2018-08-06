#!/usr/bin/env python
import requests

class Price:
    def __init__(self):
        self.fsym = "ARK'
        self.tsyms = 'USD,EUR'
        self.url = 'https://min-api.cryptocompare.com/data/pricehistorical'

    def get_market_price(ts):
        # set request params
        params = {"fsym": self.fsym,
                  "tsyms": self.tsyms,
                  "ts": ts}

        r = requests.get(self.url, params=params)

        output = [ts, r.json()['ARK']['USD'], r.json()['ARK']['EUR']]

        return output