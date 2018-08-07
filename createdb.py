from core.taxdb import TaxDB
from util.config import use_network
import os.path

if __name__ == "__main__":

    n = use_network("ark")
    # check to see if tax.db exists, if not initialize db, etc
    if os.path.exists('tax.db') == False:
        taxdb = TaxDB(n['dbuser'])
        # initalize sqldb object
        taxdb.setup()
        
        #setup initial delegate and prices 
        d = psql.get_delegates()
        p = Price()
        t = int(time.time())

        # price = [p.get_market_price(t)]
        addresses = [i[0] for i in d]

        taxdb.update_prices(price)
        taxdb.update_delegates(addresses)
