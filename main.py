import json

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Book, Author, Category, BookAuthor, BookCategory
import os

# dbUrl = os.environ["DATABASE_URL"]

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

# Session = sessionmaker(bind=create_engine("postgresql://localhost:5432/test_library"))
# session = Session()
engine = create_engine("postgresql://localhost:5432/test_library")
Session = sessionmaker(bind=engine)
session = Session()


# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@app.route('/books', methods=['GET'])
def get_all_books():
    books = session.query(Book).all()
    result = []

    for book in books:
        # categories = session.query(Category).join(BookCategory, BookCategory.book_id == book.id)
        # authors = session.query(Author).join(BookAuthor, BookAuthor.book_id == book.id)
        result.append({
            "title": book.title,
            "categories": [category.name for category in book.categories],
            "authors": [author.name for author in book.authors],
            "pages": book.pages
        })

    return json.dumps({"Books": result}), 200


@app.route('/books/<int:book_id>', methods=['GET'])
def get_specific_book(book_id):
    if type(book_id) is not int or book_id <= 0:
        return json.dumps({"Message": "Invalid book id"}), 400

    book = session.query(Book).filter(Book.id == book_id).first()

    if book is None:
        return json.dumps({"Message": "Book with given id does not exist"}), 400

    return json.dumps({"Book": {
        "title": book.title,
        "categories": [category.name for category in book.categories],
        "authors": [author.name for author in book.authors],
        "pages": book.pages
    }}), 200


@app.route('/books/remove/<int:book_id>', methods=['POST'])
def remove_book(book_id):
    if type(book_id) is not int or book_id <= 0:
        return json.dumps({"Message": "Invalid book id"}), 400

    book = session.query(Book).filter(Book.id == book_id).first()

    if book is None:
        return json.dumps({"Message": "Book with given id does not exist"}), 400

    session.delete(book)
    session.commit()

    return Response(status=200)


# @app.route('/books/edit/<int:id>', methods=['POST'])
# def edit_book(id):
#     pass
#
#
@app.route('/create_author', methods=['POST'])
def create_author():
    name = request.json.get("name", "")

    if len(name) == 0:
        return json.dumps({"Message": "Invalid field name"}), 400

    author = Author(name=name)
    session.add(author)
    session.commit()

    return Response(status=200)


@app.route('/authors', methods=['GET'])
def get_all_authors():
    authors = session.query(Author).all()

    result = [auth.name for auth in authors]

    return json.dumps({"Authors": result})


@app.route('/create_category', methods=['POST'])
def create_category():
    name = request.json.get("name", "")

    if len(name) == 0:
        return json.dumps({"Message": "Invalid field name"}), 400

    category = Category(name=name)
    session.add(category)
    session.commit()

    return Response(status=200)


@app.route('/books/add', methods=['POST'])
def add_book():
    title = request.json.get("title", "")
    authors = request.json.get("authors", None)
    categories = request.json.get("categories", None)
    pages = request.json.get("pages", None)

    if len(title) == 0:
        return json.dumps({"Message": "Invalid field title"}), 400
    if authors is None or len(authors) == 0:
        return json.dumps({"Message": "Invalid field authors"}), 400
    if categories is None or len(categories) == 0:
        return json.dumps({"Message": "Invalid field categories"}), 400
    if pages is None or type(pages) is not int:
        return json.dumps({"Message": "Invalid field pages"}), 400

    book = Book(title=title, pages=pages)
    session.add(book)
    session.commit()

    for author_id in authors:
        if type(author_id) is not int or author_id < 0:
            continue
        author = session.query(Author).filter(Author.id == author_id).first()

        if author is None:
            continue

        book_author = BookAuthor(author_id=author.id, book_id=book.id)
        session.add(book_author)
        session.commit()

    for category_id in categories:
        if type(category_id) is not int or category_id < 0:
            continue
        category = session.query(Category).filter(Category.id == category_id).first()

        if category is None:
            continue

        book_category = BookCategory(category_id=category.id, book_id=book.id)
        session.add(book_category)
        session.commit()

    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
