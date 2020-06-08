from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:b5819@localhost/bookify_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class BooksAuthors:
    def __init__(self, title, author, year, topic, cover_url):
        self.title = title
        self.author = author
        self.year = year
        self.topic = topic
        self.cover_url = cover_url

class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    topic = db.Column(db.String(100))
    cover_url = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id"))

    # def __repr___(seft):
    #     return "<Books %r>" % self.title

class Authors(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200))
    books = db.relationship("Books", backref="authors", lazy=True)

    # def __repr___(seft):
    #     return "<Authors %r>" % self.name

@app.route("/")
def index():

    books = []

    books_db = Books.query.all()

    for book in books_db:
        author_db = Authors.query.filter_by(author_id=book.author_id).first()
        books.append(BooksAuthors(book.title, author_db.name, book.year, book.topic, book.cover_url)) 

    context = {
        "books": books,
    }

    return render_template("index.html", **context)


@app.route("/add")
def add_Book():
    return "Add book"


@app.route("/delete")
def delete_Book():
    return "Delete book"


@app.route("/edit")
def edit_Book():
    return "Edit a book"