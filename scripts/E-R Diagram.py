from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Movie Booking System ER Diagram')

# Define nodes (Entities)
entities = {
    'User': ['id', 'username', 'email', 'password_hash'],
    'Movie': ['id', 'title', 'genres', 'actor', 'start_date', 'end_date'],
    'Theater': ['id', 'name', 'rows', 'seats_per_row'],
    'Showtime': ['id', 'start_time', 'movie_id', 'theater_id'],
    'Seat': ['id', 'row', 'number', 'status', 'locked_by', 'locked_until', 'showtime_id', 'booking_id'],
    'Booking': ['id', 'user_id', 'showtime_id', 'status', 'created_at'],
    'Payment': ['id', 'booking_id', 'amount', 'status', 'timestamp']
}

# Add entity nodes
for entity, fields in entities.items():
    label = f"{entity}|{'|'.join(fields)}"
    dot.node(entity, label=f"{{{label}}}", shape='record')

# Define relationships
relationships = [
    ('User', 'Booking', '1:N'),
    ('Movie', 'Showtime', '1:N'),
    ('Theater', 'Showtime', '1:N'),
    ('Showtime', 'Seat', '1:N'),
    ('Showtime', 'Booking', '1:N'),
    ('Booking', 'Payment', '1:1'),
    ('Booking', 'Seat', '1:N', 'via booking_id')
]

# Add edges for relationships
for src, dst, rel, *note in relationships:
    label = rel + (f" ({note[0]})" if note else '')
    dot.edge(src, dst, label=label)

# Render the diagram
output_path = "/mnt/data/fixed_movie_booking_er_diagram"
dot.render(output_path, format='png', cleanup=False)
output_path += ".png"  # Append the file extension for display

output_path
