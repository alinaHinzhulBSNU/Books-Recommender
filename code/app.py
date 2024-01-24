import os
import json
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


# SETTINGS

app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SECRET_KEY"] = "thisisasecretkey"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

BOOKS_PER_PAGE = 12


# MODELS

# Tables (many-to-many)
theme = db.Table("theme",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key = True, nullable=False),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key = True, nullable=False)
)

authors = db.Table("authors",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key = True, nullable=False),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key = True, nullable=False)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(255), unique=True, nullable=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String(255), unique=True, nullable=False)
    books = db.relationship("Book", secondary=authors, backref="authors")

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publisher_name = db.Column(db.String(255), unique=True, nullable=False)
    books = db.relationship("Book", backref="publisher")
  
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False)
    isbn = db.Column(db.String(255), nullable=False)
    book_title = db.Column(db.String(255), unique=True, nullable=False)
    age_limit = db.Column(db.String(255), nullable=False)
    is_for_school = db.Column(db.Boolean, nullable=False)
    language = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=True)
    original_book_title = db.Column(db.String(255), nullable=True)
    size = db.Column(db.String(255), nullable=True)
    weight = db.Column(db.String(255), nullable=True)
    cover = db.Column(db.String(255), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(5000), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(255), nullable=False)
    tags = db.relationship("Tag", secondary=theme, backref="books")
    actions = db.relationship("Action", backref="book")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    actions = db.relationship("Action", backref="user")

class Action(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)


# FORMS
    
class RegistrationForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    
    password = PasswordField(label="Password",
                             validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError("This username already exists.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")


# ROUTES

@app.route('/')
@login_required
def home():
    return redirect(url_for("page", page_number=1))

@app.route('/page-<int:page_number>')
@login_required
def page(page_number):
    pages = range(1, Book.query.count() // BOOKS_PER_PAGE + 2)
    books = Book.query.paginate(page=page_number, per_page=BOOKS_PER_PAGE, error_out=False).items

    return render_template('home.html', books = books, pages=pages, current_page=page_number)

@app.route('/book-<int:book_id>')
@login_required
def book(book_id):
    book = Book.query.filter_by(id = book_id).first()
    return render_template('book.html', book = book)

@app.route('/login', methods=["GET", "POST"])
def login():
    try:
       id = current_user.id
       return redirect(url_for("home"))
    except Exception:
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for("home"))

        return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    try:
       id = current_user.id
       return redirect(url_for("home"))
    except:         
        form = RegistrationForm()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))

        return render_template('register.html', form=form)


@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# DATA

def add_data_to_db():

    # context
    app.app_context().push()
    
    # schema
    db.create_all()
    
    with open("clean_json_data/books.json", "r") as file:
        books_json = json.load(file)

        for book_json in books_json:
            # Publisher
            publisher_name = book_json["Видавництво"]

            publisher = Publisher.query.filter_by(publisher_name=publisher_name).first()
            if not publisher:
                publisher = Publisher(publisher_name = publisher_name)
                db.session.add(publisher)

            # Authors
            authors = list()
            authors_names = book_json["Автори"]
            for author_name in authors_names:
                author = Author.query.filter_by(author_name=author_name).first()
                if not author:
                    author = Author(author_name = author_name)
                    db.session.add(author)
                    authors.append(author)

            # Tags
            tags = list()
            tags_names = book_json["Теги"]
            for tag_name in tags_names:
                tag = Tag.query.filter_by(tag=tag_name).first()
                if not tag:
                    tag = Tag(tag = tag_name)
                    db.session.add(tag)
                    tags.append(tag)

            # Book
            isbn_text = book_json["ISBN"]

            book_title = book_json["title"]

            age_limit = "універсальна"
            if "Вік" in book_json.keys():
                age_limit = book_json["Вік"]

            is_for_school = False
            if "Шкільна програма" in book_json.keys():
                is_for_school = True

            language = "українська"
            if "Мова" in book_json.keys():
                language = book_json["Мова"]

            pages_number = book_json["Сторінки"]

            price = None
            if "Паперова" in book_json["price"]:
                price = book_json["price"]["Паперова"]
                if price != "":
                    price = float(price.replace("грн", "").strip())
                else:
                    price = None
            elif book_json["price"] != "":
                price = float(book_json["price"].split(' ')[0].replace("грн", "").strip().replace(",", ""))
            else:
                price = None

            original_book_title = None
            if "Оригінальна назва" in book_json.keys():
                original_book_title = book_json["Оригінальна назва"]

            size = book_json["Розмір"]

            weight = None
            if "Вага" in book_json.keys():
                weight = book_json["Вага"]

            cover = None
            if "Палітурка" in book_json.keys():
                cover = book_json["Палітурка"]

            year = None
            if "Рік видання" in book_json.keys():
                try:
                    year = int(book_json["Рік видання"])
                except:
                    year = None
        
            description = book_json["description"]

            url = book_json["url"]

            cover_url = book_json["cover_img"]

            book = Book.query.filter_by(book_title=book_title).first()
            if not book:
                try:
                    book = Book(isbn = isbn_text,
                                book_title = book_title,
                                age_limit = age_limit,
                                is_for_school = is_for_school,
                                language = language,
                                pages = pages_number,
                                price = price,
                                original_book_title = original_book_title,
                                size = size,
                                weight = weight,
                                cover = cover,
                                year = year,
                                description = description,
                                url = url,
                                cover_url = cover_url)
                    book.tags = tags
                    book.authors = authors
                    book.publisher = publisher

                    db.session.add(book)
                except:
                    print(price)

            db.session.commit()
        

if __name__ == '__main__':
    if not os.path.isfile("instance/books.db"):
        print("Initialize DB")
        add_data_to_db()

    app.run(port=8000, debug=True)