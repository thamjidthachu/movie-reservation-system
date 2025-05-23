from flask import Blueprint, jsonify, request
from .models import Movie, Showtime, Seat
from .extensions import db

main = Blueprint('main', __name__)

@main.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.title for movie in movies])

@main.route('/movies/<int:id>/showtimes', methods=['GET'])
def get_showtimes(id):
    showtimes = Showtime.query.filter_by(movie_id=id).all()
    return jsonify([showtime.start_time.isoformat() for showtime in showtimes])

@main.route('/showtimes/<int:id>/seats', methods=['GET'])
def get_seats(id):
    seats = Seat.query.filter_by(showtime_id=id).all()
    return jsonify([{'row': seat.row, 'number': seat.number, 'status': seat.status} for seat in seats])

@main.route('/reserve', methods=['POST'])
def reserve_seat():
    data = request.get_json()
    seat = Seat.query.get(data['seat_id'])
    if seat and seat.status == 'available':
        seat.status = 'reserved'
        db.session.commit()
        return jsonify({'message': 'Seat reserved successfully'})
    return jsonify({'message': 'Seat not available'}), 400
