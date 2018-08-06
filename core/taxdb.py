#!/usr/bin/env python
import psycopg2

class DB:
    def __init__(self, db, u, pw):
        self.connection = psycopg2.connect(
            dbname = db,
            user = u,
            password= pw,
            host='localhost',
            port='5432'
        )
        
        self.cursor=self.connection.cursor()