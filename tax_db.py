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
                self.cursor.execute(f"""SELECT * FROM transactions WHERE "recipientId" = {account}""")
            else:
                self.cursor.execute(f"""SELECT * FROM transactions WHERE "senderId" = {account}""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)