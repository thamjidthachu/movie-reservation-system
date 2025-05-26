from flask import Flask
from flask_jwt_extended import JWTManager

from .auth import auth
from .extensions import db, socketio, migrate
from .routes import movie
from .socket import socketio_events

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app)

    from flask_cors import CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')

    app.register_blueprint(movie)

    # Register Socket.IO events
    socketio_events(socketio)

    return app
