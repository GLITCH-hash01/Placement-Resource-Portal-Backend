from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import config
from .database import db
from .models import Users
from flask_cors import CORS


def create_app():
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    Migrate(app,db)
    JWTManager(app)
    CORS(app,resources={r"/*": {"origins": "*"}},supports_credentials=True)
   

    from .routes.auth import auth
    from .routes.notes import notes_bp
    from .routes.events import events_bp

    app.register_blueprint(auth,url_prefix='/auth')
    app.register_blueprint(notes_bp,url_prefix='/notes')
    app.register_blueprint(events_bp,url_prefix='/events')

    return app
