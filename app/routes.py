from flask import Blueprint, jsonify, request
from .models import Movie, Showtime, Seat
from .extensions import db

main = Blueprint('main', __name__)


@main.route('/movies', methods=['GET', 'POST'])
def handle_movies():
    if request.method == 'GET':
        # Grab query parameters
        browse = request.args.get('browse')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        actor = request.args.get('actor')
        genre = request.args.get('genre')

        # Start with the base query
        query = Movie.query

        # Apply filters only if the params are provided from filter
        if start_date:
            query = query.filter(Movie.start_date >= start_date)

        if end_date:
            query = query.filter(Movie.end_date <= end_date)

        if actor:
            query = query.filter(Movie.actor == actor)

        if genre:
            query = query.filter(Movie.genres == genre)

        # Apply filters only if the params are provided from search
        if browse:
            search_term = f'%{browse}%'
            query = query.filter(
                db.or_(
                    Movie.actor.ilike(search_term), Movie.genres.ilike(search_term), Movie.title.ilike(search_term)
                )
            )

        movies = query.all()
        return jsonify([movie.to_dict() for movie in movies])

    if request.method == 'POST':
        data = request.get_json()
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        try:
            new_movie = Movie(
                title=data['title'],
                actor=data.get('actor'),
                start_date=data.get('start_date'),
                end_date=data.get('end_date'),
                genres=data.get('genres')
            )
            db.session.add(new_movie)
            db.session.commit()
            return jsonify(new_movie.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    return None


@main.route('/movies/<int:id>/show-times', methods=['GET'])
def get_show_times(id):
    show_times = Showtime.query.filter_by(movie_id=id).all()
    return jsonify([showtime.start_time.isoformat() for showtime in show_times])


@main.route('/show-times/<int:id>/seats', methods=['GET'])
def get_seats(show_id):
    seats = Seat.query.filter_by(showtime_id=show_id).all()
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
