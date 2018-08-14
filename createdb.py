from core.taxdb import TaxDB
from core.psql import DB
from core.price import Price
from util.config import use_network
import os.path
import time


day = 86400

if __name__ == "__main__":

    n = use_network("ark")
    # check to see if tax.db exists, if not initialize db, etc
    if os.path.exists('tax.db') == False:
        taxdb = TaxDB(n['dbuser'])
        psql = DB(n['database'], n['dbuser'], n['dbpassword'])
        taxdb.setup()
        
        #setup initial delegates
        d = psql.get_delegates()
        addresses = [i[0] for i in d]
        taxdb.update_delegates(addresses)

        # get prices
        p = Price()
        t = int(time.time())			
        newEpoch = get_offset(epoch)
        timestamps = get_timestamps(newEpoch, t)

        for i in timestamps:
            price = [p.get_market_price(i)]
            taxdb.update_prices(price)

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