from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm
# from wtforms.fields import StringField, SubmitField
# from wtforms.validators import DataRequired, URL

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

# class AddBook(FlaskForm):
#     title = StringField(u"Title", validators=[DataRequired()], render_kw={"ng-madel":"NameModel"})
#     author = StringField("Author", validators=[DataRequired()])
#     year = StringField("Year", validators=[DataRequired()])
#     topic = StringField("Topic", validators=[DataRequired()])
#     cover_url = StringField("Cover URL", validators=[URL(), DataRequired()])
#     submit = SubmitField("Save changes")

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


@app.route("/", defaults={"book_id_url":-1}, methods=["POST", "GET"])
@app.route("/<book_id_url>", methods=["POST", "GET"])
def index(book_id_url):

    books = []
    
    # book_data = AddBook()

    books_db = Books.query.all()

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
        book_toedit = Books.query.filter_by(book_id=book_id_url).first()

        book_edited = request.form

        book_toedit.title = book_edited["title"]
        book_toedit.year = book_edited["year"]
        book_toedit.topic = book_edited["topic"]
        book_toedit.cover_url = book_edited["cover_url"]

        db.session.commit()

        return redirect(url_for("index"))
        
    context = {
        "books": books,
        # "book_data": book_data 
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