from flask import Flask
from .extensions import db, socketio, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    from .routes import main  # 👈 Import the blueprint
    app.register_blueprint(main)  # 👈 Register it here

    from .socket import socketio_events  # import your socketio event handlers
    socketio_events(socketio)  # pass socketio instance here

    return app
