from core.taxdb import TaxDB
from core.psql import DB
from core.price import Price
from util.config import use_network
import os.path


day = 86400

if __name__ == "__main__":

    n = use_network("ark")
    # check to see if tax.db exists, if not initialize db, etc
    if os.path.exists('tax.db') == False:
        taxdb = TaxDB(n['dbuser'])
        psql = DB(n['database'], n['dbuser'], n['dbpassword'])
        taxdb.setup()
        
        #setup initial delegate and prices 
        d = psql.get_delegates()
        p = Price()
        t = int(time.time())			
        newEpoch = get_offset(epoch)
	
        # price = [p.get_market_price(t)]
        addresses = [i[0] for i in d]

        taxdb.update_prices(price)
        taxdb.update_delegates(addresses)

def get_offset(e):
    offset = 0
    while ((e+offset) % day) != 0:	
	offset += 1	
	
    return (e+offset)

def get_timestamps(first, ts):
