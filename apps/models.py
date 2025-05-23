from datetime import datetime
from .extensions import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    genres = db.Column(db.String(200))
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    seats = db.relationship('Seat', backref='showtime', lazy=True)

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.String(1), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='available')
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
