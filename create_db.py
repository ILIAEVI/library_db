import sqlite3

conn = sqlite3.connect('library.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS author (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_date DATE NOT NULL,
        birth_place TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category_name TEXT NOT NULL,
        page_quantity INTEGER NOT NULL,
        publish_date DATE NOT NULL,
        author_id INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES author (id)
    );
''')

conn.commit()

conn.close()

print("Database and tables created successfully.")
