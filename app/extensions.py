import jwt
from flask import request, current_app
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")
user_socket_map = {}


def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None

@socketio.on('connect')
def handle_connect():
    token = request.args.get("token")
    if token:
        user_id = decode_token(token)["sub"]
        user_socket_map[user_id] = request.sid
