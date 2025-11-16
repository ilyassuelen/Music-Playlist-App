from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    cover_url = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)