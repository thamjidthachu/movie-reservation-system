import csv
from app import create_app
from app.models import db, Movie, Theater, Showtime, Seat
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Insert Movies
    with open("data/movies.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie = Movie(
                id=int(row["id"]),
                title=row["title"],
                genres=row["genres"],
                actor=row["actor"],
                start_date=datetime.fromisoformat(row["start_date"]),
                end_date=datetime.fromisoformat(row["end_date"])
            )
            db.session.add(movie)

    # Insert Theaters
    with open("data/theaters.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            theater = Theater(
                id=int(row["id"]),
                name=row["name"],
                rows=int(row["rows"]),
                seats_per_row=int(row["seats_per_row"])
            )
            db.session.add(theater)

    # Insert Showtimes
    with open("data/showtimes.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            showtime = Showtime(
                id=int(row["id"]),
                movie_id=int(row["movie_id"]),
                theater_id=int(row["theater_id"]),
                start_time=datetime.fromisoformat(row["start_time"])
            )
            db.session.add(showtime)

    # Insert Seats
    with open("data/seats.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            seat = Seat(
                id=int(row["id"]),
                row=row["row"],
                number=int(row["number"]),
                status=row["status"],
                showtime_id=int(row["showtime_id"])
            )
            db.session.add(seat)

    db.session.commit()
    print("✅ Sample data inserted!")
