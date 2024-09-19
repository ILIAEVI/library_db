import sqlite3
import pandas as pd

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def get_book_with_most_pages():
    cursor.execute(
        '''
        SELECT * FROM book
        ORDER BY page_quantity DESC
        LIMIT 1;
        '''
    )
    book = cursor.fetchone()
    if book:
        return {
            "ID": book[0],
            "Name": book[1],
            "Category Name": book[2],
            "Page Quantity": book[3],
            "Publish Date": book[4],
            "Author ID": book[5]
        }
    else:
        return None

def get_avg_page_quantity():
    cursor.execute(
        '''
        SELECT AVG(page_quantity) FROM book;
        '''
    )
    avg_pages = cursor.fetchone()[0]
    return {"Average Page Quantity": avg_pages}


def get_youngest_author():
    cursor.execute(
        '''
        SELECT * FROM author
        ORDER BY strftime('%Y', 'now') - strftime('%Y', birth_date) DESC
        LIMIT 1;
        '''
    )
    author = cursor.fetchone()
    if author:
        return {
            "ID": author[0],
            "Name": author[1],
            "Last Name": author[2],
            "Birth Date": author[3],
            "Birth Place": author[4]
        }
    return None

def get_authors_without_books():
    cursor.execute(
        '''
        SELECT author.id, author.name, author.last_name, author.birth_date, author.birth_place
        FROM author
        LEFT JOIN book ON author.id = book.author_id
        WHERE book.author_id IS NULL;
        '''
    )
    authors = cursor.fetchall()
    return[
        {
            "ID": author[0],
            "Name": author[1],
            "Last Name": author[2],
            "Birth Date": author[3],
            "Birth Place": author[4]
        }
    for author in authors
    ]


def find_authors_with_three_or_more_book():
    cursor.execute(
        '''
        SELECT author.id, author.name, author.last_name, author.birth_date, author.birth_place, COUNT(book.id) AS book_count
        FROM author
        JOIN book ON author.id = book.author_id
        GROUP BY author.id
        HAVING COUNT(book.id) >= 3
        LIMIT 5;
        '''
    )
    authors = cursor.fetchall()
    return [
        {
            "ID": author[0],
            "Name": author[1],
            "Last Name": author[2],
            "Birth Date": author[3],
            "Birth Place": author[4],
            "Book Count": author[5]
        }
        for author in authors
    ]

def print_book_with_most_pages(book):
    if book:
        print("Book with the Most Pages:")
        print(f"ID: {book['ID']}")
        print(f"Name: {book['Name']}")
        print(f"Category Name: {book['Category Name']}")
        print(f"Page Quantity: {book['Page Quantity']}")
        print(f"Publish Date: {book['Publish Date']}")
        print(f"Author ID: {book['Author ID']}")
    else:
        print("No book found.")

def print_average_page_quantity(average_page_quantity):
    print(f"Average Page Quantity: {average_page_quantity['Average Page Quantity']:.2f}")

def print_youngest_author(author):
    if author:
        print("Youngest Author:")
        print(f"ID: {author['ID']}")
        print(f"Name: {author['Name']}")
        print(f"Last Name: {author['Last Name']}")
        print(f"Birthday: {author['Birth Date']}")
        print(f"Birth Place: {author['Birth Place']}")
    else:
        print("No author found.")

def print_authors_without_books(authors):
    print('Authors without Books:')
    if authors:
        for author in authors:
            print(f"ID: {author['ID']}")
            print(f"Name: {author['Name']}")
            print(f"Last Name: {author['Last Name']}")
            print(f"Birthday: {author['Birth Date']}")
            print(f"Birth Place: {author['Birth Place']}")

def print_authors_with_three_or_more_book(authors):
    if authors:
        print("Authors with 3 or more books:")
        for author in authors:
            print(f"ID: {author['ID']}")
            print(f"Name: {author['Name']}")
            print(f"Last Name: {author['Last Name']}")
            print(f"Birthday: {author['Birth Date']}")
            print(f"Birth Place: {author['Birth Place']}")
            print(f"Book Count: {author['Book Count']}")

book_most_pages = get_book_with_most_pages()
avg_page_quantity = get_avg_page_quantity()
youngest_author = get_youngest_author()
authors_without_books = get_authors_without_books()
authors_with_three_or_more_book = find_authors_with_three_or_more_book()


with pd.ExcelWriter('report.xlsx', engine='openpyxl') as writer:
    if authors_without_books:
        df_author = pd.DataFrame([authors_without_books])
        df_author.to_excel(writer, sheet_name='Author without Books', index=False)


conn.close()

print('Excel File created successfully!')

print_book_with_most_pages(book_most_pages)
print('--------------')
print_average_page_quantity(avg_page_quantity)
print('--------------')
print_youngest_author(youngest_author)
print('--------------')
print_authors_without_books(authors_without_books)
print('--------------')
print_authors_with_three_or_more_book(authors_with_three_or_more_book)
