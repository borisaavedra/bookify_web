from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "A QUe No la AdivinAS"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///bookify_db.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class BooksAuthors:
    def __init__(self, book_id, title, author_id, author, year, topic, cover_url, book_count, country):
        self.book_id = book_id
        self.title = title
        self.author_id = author_id
        self.author = author
        self.year = year
        self.topic = topic
        self.cover_url = cover_url
        self.book_count = book_count
        self.country = country


class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    topic = db.Column(db.String(100))
    cover_url = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id"), nullable=False)


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
            book.cover_url,
            book_count=0,
            country = "0"
        )) 

    if request.method == "POST":
        book_toedit = Books.query.filter_by(book_id=book_id_url).first()
        if int(delete):
            db.session.delete(book_toedit)

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
            print(new_book["author"])
            db.session.commit()
            flash("Book added! 🤘", "success")
            return redirect(url_for("add_Book"))
        except:
            flash("Something went wrong 😓. Please try again", "danger")
            return redirect(url_for("add_Book"))

    return render_template("add-book.html", **context)


@app.route("/add-author", defaults={"author_id_url":-1, "delete": 0}, methods=["POST", "GET"])
@app.route("/add-author/<author_id_url>/<delete>", methods=["POST", "GET"])
def add_Author(author_id_url, delete):

    authors_db = Authors.query.all()
    authors = []

    for author in authors_db:
        num_books = Books.query.filter_by(author_id=author.author_id).count()
        authors.append(
            BooksAuthors(
                author_id = author.author_id,
                author = author.name,
                country = author.country,
                book_count = num_books,
                book_id = 0,
                title = "0",
                year = 0,
                topic = "0",
                cover_url = "0"
            )
        )
        
    if request.method == "POST":
            author_toedit = Authors.query.filter_by(author_id=author_id_url).first()
            if int(delete):
                print("----> DELETE AUTHOR")
                db.session.delete(author_toedit)
                try:
                    db.session.commit()
                    flash("Author deleted 😮", "success")
                    return redirect(url_for("add_Author"))
                except:
                    flash("Something went wrong 😓", "danger")
            elif int(author_id_url) > 0:
                author_edited = request.form
                author_toedit.name = author_edited["author"]
                author_toedit.country = author_edited["country"]

                try:
                    db.session.commit()
                    flash("Author edited successfuly 😎", "success")
                    return redirect(url_for("add_Author"))
                except:
                    flash("Something went wrong 😓", "danger")
            else:
                author_toadd = request.form
                print(author_toadd["author"])
                new_author = Authors(name=author_toadd["author"], country=author_toadd["country"])
                db.session.add(new_author)
            try:
                db.session.commit()
                flash("New Author added 😎", "success")
                return redirect(url_for("add_Author"))
            except:
                flash("Something went wrong 😯", "danger")

    context = {
        "authors": authors,
    }

    return render_template("add-author.html", **context)


# if __name__ == "__main__":
#     db.create_all()
#     app.run()