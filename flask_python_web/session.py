from flask import Flask, redirect, session ,url_for, render_template, request, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAIchemy
from os import path

app = Flask(__name__)
app.config["SECRET_KEY"] = "kiendz"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.permanent_session_lifetime = timedelta(minutes=10)

db = SQLAlchemy(app)
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        user_email = request.form["email"]
        session.permanent = True
        if user_name:
            session["user"] = user_name
            return redirect(url_for("user.html", user=user_name))
        if "user" in session:
            name = session["user"]
            return redirect(url_for("user.html", user=user_name))
    return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        name = session["user"]
        return render_template("user.html", user=name)
    else:
        flash("You haven't already logged in! ", "info")
        return redirect(url_for("login"))
    

@app.route("/logout")
def log_out():
    flash("You logged out! ", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__=="__main__":
    if not path.exists("users.db"):
        db.create_all()
    app.run(debug=True)
    