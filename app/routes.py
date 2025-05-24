from datetime import datetime

import stripe
from flask import Blueprint, jsonify, request
from flask import current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from .extensions import db
from .models import Movie, Showtime, Seat, Booking

movie = Blueprint('main', __name__)


@movie.route('/movies', methods=['GET', 'POST'])
# @jwt_required()
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


@movie.route('/movie/<int:movie_id>/show-times', methods=['GET'])
def get_show_times(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    data = []
    for showtime in movie.show_times:
        total_seats = Seat.query.filter_by(showtime_id=showtime.id).count()
        available_seats = Seat.query.filter_by(showtime_id=showtime.id, status='available').count()

        data.append({
            'showtime_id': showtime.id,
            'start_time': showtime.start_time.isoformat(),
            'theater': showtime.theater.name,
            'total_seats': total_seats,
            'available_seats': available_seats
        })

    return jsonify({
        'movie_id': movie.id,
        'title': movie.title,
        'show_times': data
    })


@movie.route('/showtime/<int:showtime_id>/seats', methods=['GET'])
def get_seating_map(showtime_id):
    showtime = Showtime.query.get_or_404(showtime_id)
    seats = Seat.query.filter_by(showtime_id=showtime_id).all()

    # Organize seats by row
    seat_map = {}
    for seat in seats:
        row = seat.row
        if row not in seat_map:
            seat_map[row] = []
        seat_map[row].append({
            'id': seat.id,
            'number': seat.number,
            'status': seat.status
        })

    # Sort seats within each row
    for row in seat_map:
        seat_map[row] = sorted(seat_map[row], key=lambda x: x['number'])

    return jsonify({
        'showtime_id': showtime.id,
        'movie': showtime.movie.title,
        'theater': showtime.theater.name,
        'start_time': showtime.start_time.isoformat(),
        'seating_map': seat_map
    })


@movie.route('/checkout', methods=['POST'])
@jwt_required()
def booking_checkout():
    """
    Request JSON:
    {
        "seat_ids": [10, 11, 12]
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    seat_ids = data.get('seat_ids')

    if not seat_ids:
        return jsonify({"error": "seat_ids are required"}), 400

    now = datetime.utcnow()
    lock_until = now + current_app.config['LOCK_DURATION']

    try:
        # Lock seats only if available or expired lock
        seats = (
            Seat.query
            .filter(Seat.id.in_(seat_ids))
            .with_for_update()
            .all()
        )

        for seat in seats:
            if seat.status == 'booked':
                return jsonify({"error": f"Seat {seat.id} already booked"}), 409
            if seat.status == 'locked' and seat.locked_until and seat.locked_until > now and seat.locked_by != user_id:
                return jsonify({"error": f"Seat {seat.id} is currently locked by another user"}), 409

        # Lock the seats
        for seat in seats:
            seat.status = 'locked'
            seat.locked_by = user_id
            seat.locked_until = lock_until
            db.session.add(seat)

        # Stripe Setup
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': current_app.config['CURRENCY'],
                    'product_data': {
                        'name': f'{len(seat_ids)} Seat(s) Reservation',
                    },
                    'unit_amount': current_app.config['SEAT_PRICE'],
                },
                'quantity': len(seat_ids),
            }],
            mode='payment',
            success_url="https://aqaryaid.com/en",
            cancel_url = "https://www.facebook.com",
        )

        db.session.commit()

        return jsonify({'checkout_url': session.url}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@movie.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    """
    Request JSON:
    {
        "seat_ids": [10, 11, 12],
        "showtime_id": 5,
        "payment_method_id": "pm_xxx"
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    seat_ids = data.get('seat_ids')
    showtime_id = data.get('showtime_id')
    payment_method_id = data.get('payment_method_id')

    if not user_id or not seat_ids or not showtime_id or not payment_method_id:
        return jsonify({"error": "user_id, seat_ids, showtime_id, and payment_method_id are required"}), 400

    now = datetime.utcnow()

    try:
        seats = (
            Seat.query
            .filter(Seat.id.in_(seat_ids))
            .with_for_update()
            .all()
        )

        for seat in seats:
            if seat.status != 'locked' or seat.locked_by != user_id or not seat.locked_until or seat.locked_until < now:
                return jsonify({"error": f"Seat {seat.id} is not locked by user or lock expired"}), 409

        # Calculate total amount
        seat_price = current_app.config['SEAT_PRICE']
        amount = len(seat_ids) * seat_price
        currency = current_app.config['CURRENCY']
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

        # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method=payment_method_id,
            confirmation_method='manual',
            confirm=True,
        )

        if intent['status'] != 'succeeded':
            return jsonify({"error": "Payment failed", "stripe_status": intent['status']}), 402

        # Payment succeeded → Confirm bookings
        for seat in seats:
            booking = Booking(
                user_id=user_id,
                seat_id=seat.id,
                showtime_id=showtime_id,
                status='confirmed',
                created_at=now
            )
            db.session.add(booking)

            seat.status = 'booked'
            seat.locked_by = None
            seat.locked_until = None
            db.session.add(seat)

        db.session.commit()
        return jsonify({"message": "Booking confirmed and payment successful!"}), 200

    except stripe.error.CardError as e:
        return jsonify({"error": e.user_message}), 402

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Double booking detected, please try again"}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@movie.route('/unlock_seats', methods=['POST'])
def unlock_seats():
    """
    Request JSON:
    {
        "seat_ids": [10, 11, 12]
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    seat_ids = data.get('seat_ids')

    if not user_id or not seat_ids:
        return jsonify({"error": "user_id and seat_ids are required"}), 400

    try:
        seats = (
            Seat.query
            .filter(and_(
                Seat.id.in_(seat_ids),
                Seat.locked_by == user_id,
                Seat.status == 'locked'
            ))
            .all()
        )

        for seat in seats:
            seat.status = 'available'
            seat.locked_by = None
            seat.locked_until = None
            db.session.add(seat)

        db.session.commit()
        return jsonify({"message": "Seats released successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
