from datetime import datetime
from .extensions import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    actor = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    genres = db.Column(db.String(200))
    show_times = db.relationship('Showtime', backref='movie', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'actor': self.actor,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'genres': self.genres
        }

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
