from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine

# from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()


# database = SQLAlchemy()


class BookAuthor(Base):
    __tablename__ = "bookauthor"

    id = Column("id", Integer, primary_key=True)
    book_id = Column("book_id", Integer, ForeignKey("book.id"), nullable=False)
    author_id = Column("author_id", Integer, ForeignKey("author.id"), nullable=False)


class BookCategory(Base):
    __tablename__ = "bookcategory"

    id = Column("id", Integer, primary_key=True)
    book_id = Column("book_id", Integer, ForeignKey("book.id"), nullable=False)
    category_id = Column("category_id", Integer, ForeignKey("category.id"), nullable=False)


class Book(Base):
    __tablename__ = "book"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(256), nullable=False)
    pages = Column("pages", Integer, nullable=False)

    # categories = relationship("Category", secondary=BookCategory.__table__, back_populates="book")
    # authors = relationship("Author", secondary=BookAuthor.__table__, back_populates="book")
    #
    categories = relationship("Category", secondary=BookCategory.__table__, backref="category_books")
    authors = relationship("Author", secondary=BookAuthor.__table__, backref="written_books")


class Category(Base):
    __tablename__ = "category"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(256), nullable=False)

    books = relationship("Book", secondary=BookCategory.__table__, backref="book_categories")


class Author(Base):
    __tablename__ = "author"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(256), nullable=False)

    books = relationship("Book", secondary=BookAuthor.__table__, backref="book_authors")
