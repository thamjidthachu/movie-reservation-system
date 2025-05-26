from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genres = db.Column(db.String(200))
    actor = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    show_times = db.relationship('Showtime', backref='movie', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genres': self.genres,
            'actor': self.actor,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
        }


class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rows = db.Column(db.Integer, nullable=False)
    seats_per_row = db.Column(db.Integer, nullable=False)

    show_times = db.relationship('Showtime', backref='theater', lazy=True)


class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)

    seats = db.relationship('Seat', backref='showtime', lazy=True)
    bookings = db.relationship('Booking', backref='showtime', lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payment = db.relationship('Payment', backref='booking', uselist=False)
    seats = db.relationship('Seat', backref='booking', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('showtime_id', 'user_id', name='unique_booking_per_user_per_showtime'),
    )


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.String(1), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='available')  # available, locked, booked
    locked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    locked_until = db.Column(db.DateTime, nullable=True)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('row', 'number', 'showtime_id', name='unique_seat_per_showtime'),
    )

    def is_lock_expired(self):
        return self.locked_until and self.locked_until < datetime.utcnow()


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    checkout_id = db.Column(db.String(200))
    status = db.Column(db.String(20), default='initiated')  # success, failed, initiated
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
