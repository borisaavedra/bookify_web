from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "A QUe No la AdivinAS"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:b5819@localhost/bookify_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class BooksAuthors:
    def __init__(self, book_id, title, author_id, author, year, topic, cover_url):
        self.book_id = book_id
        self.title = title
        self.author_id = author_id
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


class Authors(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200))
    books = db.relationship("Books", backref="authors", lazy=True)


@app.route("/", defaults={"book_id_url":-1, "delete": 0}, methods=["POST", "GET"])
@app.route("/<book_id_url>/<delete>", methods=["POST", "GET"])
def index(book_id_url, delete):

    books = []

    books_db = Books.query.all()
    authors_db = Authors.query.all()

    for book in books_db:
        author_db = Authors.query.filter_by(author_id=book.author_id).first()
        books.append(BooksAuthors(
            book.book_id, 
            book.title, 
            book.author_id,
            author_db.name, 
            book.year, 
            book.topic, 
            book.cover_url)) 

    if request.method == "POST":
        if int(delete):
            book_deleted = Books.query.filter_by(book_id=book_id_url).first()
            db.session.delete(book_deleted)

            try:
                db.session.commit()
                flash("Book deleted! 😮", "success")
                return redirect(url_for("index"))
            except:
                flash("Something went wrong 😓", "danger")
                return redirect(url_for("index"))
        else:
            book_toedit = Books.query.filter_by(book_id=book_id_url).first()

            book_edited = request.form

            book_toedit.title = book_edited["title"]
            book_toedit.year = book_edited["year"]
            book_toedit.topic = book_edited["topic"]
            book_toedit.author_id = book_edited["author"]
            book_toedit.cover_url = book_edited["cover_url"]
            
            db.session.commit()

            return redirect(url_for("index"))
        
    context = {
        "books": books,
        "authors": authors_db
    }

    return render_template("index.html", **context)


@app.route("/add-book", methods=["GET", "POST"])
def add_Book():
    authors_db = Authors.query.all()

    context = {
        "authors": authors_db
    }

    if request.method == "POST":
        new_book = request.form

        book = Books(
            title=new_book["title"],
            year=new_book["year"],
            topic=new_book["topic"],
            cover_url=new_book["cover_url"],
            author_id=new_book["author"]
        )

        db.session.add(book)

        try:
            db.session.commit()
            flash("Book added! 🤘", "success")
            return redirect(url_for("add_Book"))
        except:
            flash("Something went wrong 😓", "danger")
            return redirect(url_for("add_Book"))

    return render_template("add-book.html", **context)


@app.route("/add-author")
def add_Author():
    return render_template("add-author.html")