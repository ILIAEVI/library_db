import random
import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
faker = Faker()

author_book_association = Table(
    'author_book', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('book_id', Integer, ForeignKey('book.id'))
)


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)

    books = relationship('Book', secondary=author_book_association, back_populates='authors')


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_name = Column(String)
    page_quantity = Column(Integer)
    publish_date = Column(Date)

    authors = relationship('Author', secondary=author_book_association, back_populates='books')


class Library:
    def __init__(self, db_url='sqlite:///library_2.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def generate_fake_data(self, num_authors=500, num_books=500):
        authors = [Author(
            name=faker.first_name(),
            last_name=faker.last_name(),
            birth_date=faker.date_of_birth(minimum_age=20, maximum_age=80),
            birth_place=faker.city()
        ) for _ in range(num_authors)]

        self.session.add_all(authors)
        self.session.commit()

        books = [Book(
            name=faker.catch_phrase(),
            category_name=faker.word(),
            page_quantity=random.randint(100, 1000),
            publish_date=faker.date_between(start_date='-10y', end_date='today')
        ) for _ in range(num_books)]

        self.session.add_all(books)
        self.session.commit()

        for book in books:
            num_authors_for_book = random.randint(1, 3)
            selected_authors = random.sample(authors, num_authors_for_book)
            for author in selected_authors:
                book.authors.append(author)

        self.session.commit()

    def get_book_with_most_pages(self):
        book = self.session.query(Book).order_by(Book.page_quantity.desc()).first()
        if book:
            return {
                "ID": book.id,
                "Name": book.name,
                "Category Name": book.category_name,
                "Page Quantity": book.page_quantity,
                "Publish Date": book.publish_date,
                "Authors": ', '.join([f"{author.name} {author.last_name}" for author in book.authors])
            }
        return None

    def get_avg_page_quantity(self):
        avg_pages = self.session.query(func.avg(Book.page_quantity)).scalar()
        return {"Average Page Quantity": avg_pages}

    def get_youngest_author(self):
        author = self.session.query(Author).order_by(Author.birth_date.desc()).first()
        return {
            "ID": author.id,
            "Name": author.name,
            "Last Name": author.last_name,
            "Birth Date": author.birth_date,
            "Birth Place": author.birth_place
        } if author else None

    def get_authors_without_books(self):
        authors = self.session.query(Author).outerjoin(author_book_association).filter(
            author_book_association.c.book_id == None).all()
        return [
            {
                "ID": author.id,
                "Name": author.name,
                "Last Name": author.last_name,
                "Birth Date": author.birth_date,
                "Birth Place": author.birth_place
            }
            for author in authors
        ]

    def find_authors_with_three_or_more_books(self):
        authors = self.session.query(Author, func.count(author_book_association.c.book_id).label('book_count')) \
            .join(author_book_association) \
            .group_by(Author.id) \
            .having(func.count(author_book_association.c.book_id) >= 3) \
            .limit(5) \
            .all()
        return [
            {
                "ID": author[0].id,
                "Name": author[0].name,
                "Last Name": author[0].last_name,
                "Birth Date": author[0].birth_date,
                "Birth Place": author[0].birth_place,
                "Book Count": author[1]
            }
            for author in authors
        ]

    def close(self):
        self.session.close()


def main():
    library = Library()

    if library.session.query(Book).count() == 0 or library.session.query(Author).count() == 0:
        library.generate_fake_data()

    authors_without_books = library.get_authors_without_books()

    with pd.ExcelWriter('library_report.xlsx', engine='openpyxl') as writer:
        if authors_without_books:
            pd.DataFrame(authors_without_books).to_excel(writer, sheet_name='Authors without Books', index=False)
            print("Authors without books have been written to the Excel file.")
        else:
            print("No authors without books to write to the Excel file.")

    book_most_pages = library.get_book_with_most_pages()
    avg_page_quantity = library.get_avg_page_quantity()
    youngest_author = library.get_youngest_author()
    authors_with_three_or_more_books = library.find_authors_with_three_or_more_books()

    library.close()

    print('Excel File created successfully!')

    if book_most_pages:
        print("Book with the Most Pages:")
        print(book_most_pages)
    print('--------------')
    print(f"Average Page Quantity: {avg_page_quantity['Average Page Quantity']:.2f}")
    print('--------------')
    if youngest_author:
        print("Youngest Author:")
        print(youngest_author)
    print('--------------')
    print('Authors without Books:')
    for author in authors_without_books:
        print(author)
    print('--------------')
    print("Authors with 3 or more books:")
    for author in authors_with_three_or_more_books:
        print(author)


if __name__ == "__main__":
    main()
