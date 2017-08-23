import psycopg2

DBNAME = "catalog"

def get_books():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select name, description from books order by name")
    return c.fetchall()
    db.close()

def add_book(book):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("insert into books values (%s)",(book,))
    db.commit()
    db.close()
