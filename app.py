from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt()

# Define your database models (User and Note) using SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Your encryption and decryption functions go here

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle user registration and save hashed password to the database
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle user login and session management
        return redirect(url_for('notes'))
    return render_template("login.html")

@app.route("/notes", methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        # Handle user note creation and encryption
        flash('Your note has been encrypted and saved!', 'success')
    return render_template("notes.html")

if __name__ == '__main__':
    app.run(debug=True)

