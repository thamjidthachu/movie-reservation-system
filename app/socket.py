from flask_socketio import SocketIO

socketio = SocketIO()


def socketio_events(socketio):
    @socketio.on('seat_lock')
    def handle_seat_lock(data):
        # handle event here
        print(data)

    @socketio.on('seat_unlock')
    def handle_seat_unlock(data):
        # Handle seat unlock logic
        print(data)

    @socketio.on('seat_book')
    def handle_seat_book(data):
        # Handle seat booking logic
        print(data)
