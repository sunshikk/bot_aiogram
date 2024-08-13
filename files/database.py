import sqlite3 as sq

db = sq.connect("database.db")
cur = db.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        wins INTEGER,
        defeats INTEGER,
        draws INTEGER,
        moneyy INTEGER,
        numm INTEGER,
        wordd TEXT
    )
""")
db.commit()