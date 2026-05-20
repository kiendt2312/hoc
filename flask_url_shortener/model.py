from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    original_url = db.Column(
        db.String(500),
        nullable=False
    )

    short_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    clicks = db.Column(
        db.Integer,
        default=0
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )