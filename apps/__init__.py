from flask import Flask
from .extensions import db, socketio
from .routes import main
from .socket import socketio_events

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(main)

    socketio_events(app)

    return app
