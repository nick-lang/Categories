from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Books
from catalogdb import get_books, add_book

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/home/')
def Home():
    return "Home"

@app.route('/categories/')
def ListCategories():
    categories = session.query(Categories).all()
    output = ''
    for i in categories:
        output += i.name
        output += '</br>'
    return output

@app.route('/categories/<int:category_id>/')
def ListBooks(category_id):
    books = get_books()
    output = ''
    for i in books:
        output += i.name
        output += '</br>'
        output += i.description
        output += '</br>'
    return output

@app.route('/categories/<int:category_id>/new/')
def newBook(category_id):
    output = 'new book'
    return output

@app.route('/categories/<int:category_id>/<int:book_id>/edit/')
def editBook(category_id, book_id):
    output = 'edit'
    return output

@app.route('/categories/<int:category_id>/<int:book_id>/delete/')
def deleteBook(category_id, book_id):
    output = 'delete'
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
