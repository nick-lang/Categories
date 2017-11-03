from flask import Flask, render_template, request, url_for, jsonify
app = Flask(__name__)

from flask import session as login_session
import random, string

from oath2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Books

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/categories/')
def listCategories():
    categories = session.query(Categories).all()
    return render_template('categories.html', categories = categories)

@app.route('/categories/<int:category_id>/')
def listBooks(category_id):
    books = session.query(Books).filter_by(category_id = category_id).all()
    return render_template('books.html', books = books,
                                         category_id = category_id)

@app.route('/categories/<int:category_id>/new/', methods = ['GET','POST'])
def newBook(category_id):
    if request.method == 'POST':
        newItem = Books(name = request.form['name'],
                        description = request.form['description'],
                        category_id = category_id)
        session.add(newItem)
        session.commit()
        books = session.query(Books).filter_by(category_id = category_id).all()
        return render_template('books.html', books = books,
                                             category_id = category_id)
    else:
        category = session.query(Categories).filter_by(id = category_id).one()
        return render_template('newBook.html', category = category)

@app.route('/categories/<int:category_id>/<int:book_id>/edit/',
           methods =['GET','POST'])
def editBook(category_id, book_id):
    editedBook = session.query(Books).filter_by(id = book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['description']:
            editedBook.description = request.form['description']
        session.add(editedBook)
        session.commit()
        # Get books for render of listBooks
        books = session.query(Books).filter_by(category_id = category_id).all()
        return render_template('books.html', books = books,
                                             category_id = category_id)
    else:
        return render_template('editBook.html', book = editedBook,
                                                category_id = category_id)

@app.route('/categories/<int:category_id>/<int:book_id>/delete/',
           methods =['GET','POST'])
def deleteBook(category_id, book_id):
    bookToDelete = session.query(Books).filter_by(id = book_id).one()
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        # Get books for render of listBooks
        books = session.query(Books).filter_by(category_id = category_id).all()
        return render_template('books.html', books = books,
                                             category_id = category_id)
    else:
        return render_template('deleteBook.html', book = bookToDelete,
                                                  category_id = category_id)

@app.route('/categories/<int:category_id>/JSON/')
def listBooksJSON(category_id):
    books = session.query(Books).filter_by(category_id = category_id).all()
    return jsonify(Books=[i.serialize for i in books])

@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase
                    + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'Super secret key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
