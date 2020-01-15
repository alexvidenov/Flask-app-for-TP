import sqlite3

DB_NAME = 'example.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS categories
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS attractions
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        image TEXT,
        description TEXT,
        rating INTEGER,
        category_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS comments
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attraction_id INTEGER,
        message TEXT,
        FOREIGN KEY(attraction_id) REFERENCES attractions(id)
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS ratings
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attraction_id INTEGER,
        architecture_rating INTEGER,
        interior_rating INTEGER, 
        historical_value_rating INTEGER,
        rating INTEGER,
        FOREIGN KEY(attraction_id) REFERENCES attractions(id)
    )
''')

conn.commit()


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()