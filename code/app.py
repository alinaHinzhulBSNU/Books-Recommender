import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import *


# SETTINGS

app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db = SQLAlchemy(app)


# ROUTES

@app.route('/')
def home():
    return render_template('home.html')


# PROGRAM

def add_data_to_db():
    pass
    
if __name__ == '__main__':
    if not os.path.isfile("instance/books.db"):
        add_data_to_db()

    app.run(port=8000, debug=True)