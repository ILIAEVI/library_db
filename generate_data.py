from faker import Faker
import sqlite3
import random


fake = Faker()

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def generate_authors(quantity):
    authors = []
    for _ in range(quantity):
        name = fake.first_name()
        last_name = fake.last_name()
        birth_date = fake.date_of_birth(minimum_age=24, maximum_age=80).strftime('%d.%m.%Y')
        birth_place = fake.city()
        authors.append((name, last_name, birth_date, birth_place))

    cursor.executemany(
        '''
        INSERT INTO author (name, last_name, birth_date, birth_place)
        VALUES (?, ?, ?, ?);
        ''', authors)
    conn.commit()


def generate_books(quantity, authors_quantity):
    books = []
    categories = ['Fiction', 'Non-fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Biography', 'History', 'Science']
    for _ in range(quantity):
        name = fake.sentence(nb_words=3)
        category_name = random.choice(categories)
        page_quantity = random.randint(10, 1000)
        publish_date = fake.date_this_century().strftime('%Y-%m-%d')
        author_id = random.randint(1, authors_quantity)
        books.append((name, category_name, page_quantity, publish_date, author_id))

    cursor.executemany(
        '''
        INSERT INTO book (name, category_name, page_quantity, publish_date, author_id)
        VALUES (?, ?, ?, ?, ?);
        ''', books)
    conn.commit()


generate_authors(500)
generate_books(500, 500)

conn.close()

print('Done')