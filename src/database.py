import sqlite3
import time

class Database():
    def __init__(self, file) -> None:
        self.conn = None
        self._file = file

        self.create_live_table()

    def _create_connection(self):
        """ create a database connection to a SQLite database"""
        try:
            conn = sqlite3.connect(self._file)
        except sqlite3.Error as e:
            print(e)
        
        return conn

    def create_live_table(self):
        live_table = """CREATE TABLE IF NOT EXISTS live_prices (
                                name text PRIMARY KEY NOT NULL,
                                price real,
                                last_update integer
                                );"""
        try:
            conn = self._create_connection()
            cur = conn.cursor()
            cur.execute(live_table)
        except sqlite3.Error as e:
            print(e)

    def update_crypto(self, name, price):
        crypto = (name, price, int(time.time()), price, int(time.time()))
        sql = """INSERT INTO live_prices(name, price, last_update) 
                VALUES(?,?,?)
                ON CONFLICT(name) DO UPDATE 
                SET price=?, last_update=?"""

        conn = self._create_connection()
        cur = conn.cursor()
        cur.execute(sql, crypto)
        conn.commit()

    def get_all_crypto_prices(self):
        conn = self._create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM live_prices")

        rows = cur.fetchall()

        return rows


# db = Database(r"db/arbitrage.db")
# db.update_crypto("ETH", 12789)
# db.update_crypto("BCH", 127)
# print(db.get_all_crypto_prices())

# conn = create_connection(r"db/arbitrage.db")

# update_crypto(conn, "BTC", 28.8)