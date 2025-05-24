from flask import Flask
from flask_jwt_extended import JWTManager
from .extensions import db, socketio, migrate

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    migrate.init_app(app, db)

    from flask_cors import CORS
    CORS(app)

    # Register blueprints
    from .routes import movie
    app.register_blueprint(movie)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # Register Socket.IO events
    from .socket import socketio_events
    socketio_events(socketio)  # Pass the instance to event handlers

    return app
