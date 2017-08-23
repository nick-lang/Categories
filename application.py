from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Books

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/home')
def Home():
    return "Home"

@app.route('/categories')
def ListCategories():
    categories = session.query(Categories).all()
    output = ''
    for i in categories:
        output += i.name
        output += '</br>'
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
