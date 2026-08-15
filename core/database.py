import sqlite3
import os


class Database:

    def __init__(self, path="database/qmos.db"):
        self.path = path
        self.connection = None


    def connect(self):

        if not os.path.exists("database"):
            os.makedirs("database")

        self.connection = sqlite3.connect(self.path)

        self.connection.row_factory = sqlite3.Row

        return self.connection



    def close(self):

        if self.connection:

            self.connection.close()

            self.connection = None



    def execute(self, query, params=()):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        result = cursor.lastrowid

        self.close()

        return result



    def execute_many(self, query, data):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.executemany(query, data)

        conn.commit()

        self.close()



    def fetch_one(self, query, params=()):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(query, params)

        result = cursor.fetchone()

        self.close()

        return result



    def fetch_all(self, query, params=()):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(query, params)

        result = cursor.fetchall()

        self.close()

        return result



    def table_exists(self, table_name):

        query = """
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' 
        AND name=?
        """

        result = self.fetch_one(query, (table_name,))

        return result is not None



    def create_table(self, query):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(query)

        conn.commit()

        self.close()



if __name__ == "__main__":

    print("===================================")
    print("GSIS CORE DATABASE MODULE")
    print("VERSION 1.0")
    print("STATUS: READY")
    print("===================================")

    db = Database()

    if db.table_exists("candles"):

        print("Database connection: OK")
        print("Candles table detected")

    else:

        print("Database connection: OK")
        print("Candles table not found")

    print("===================================")
