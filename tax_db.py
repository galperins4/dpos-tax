import psycopg2

class TaxDB:
    def __init__(self, db, u, pw):
        self.connection = psycopg2.connect(
            dbname=db,
            user=u,
            password=pw,
            host='localhost',
            port='5432'
        )

        self.cursor = self.connection.cursor()

    def get_transactions(self, account, side):
        try:
            if side == "buy":
                self.cursor.execute(f"""SELECT "timestamp", "amount", "fee" FROM transactions WHERE "recipientId" = '{
                account}' AND "type" = {0} ORDER BY "timestamp" ASC""")
            else:
                self.cursor.execute(f"""SELECT "timestamp", "amount", "fee" FROM transactions WHERE "senderId" = '{
                account}'ORDER BY "timestamp" ASC""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            
    def get_delegates(self):
        try:
            self.cursor.execute(f"""SELECT DISTINCT "dependentId" FROM mem_accounts2delegates""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            
            
            
            
            
