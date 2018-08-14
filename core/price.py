#!/usr/bin/env python
import requests
import time

class Price:
    def __init__(self):
        self.fsym = 'ARK'
        self.tsyms = 'USD,EUR'
        self.url = 'https://min-api.cryptocompare.com/data/pricehistorical'

    def get_market_price(self, ts):
        # set request params
        params = {"fsym": self.fsym,
                  "tsyms": self.tsyms,
                  "ts": ts}

        try:
            r = requests.get(self.url, params=params)
            output = [ts, r.json()['ARK']['USD'], r.json()['ARK']['EUR']]
        except:
            output = [ts, 0, 0]
    
        time.sleep(0.25)

        return output