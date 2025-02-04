from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import config
from .database import db
from .models import Users
from flask_cors import CORS
from flask import request

def create_app():
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    Migrate(app,db)
    JWTManager(app)
    CORS(app,resources={r"/*": {"origins": "*"}},supports_credentials=True)
   

    from .routes.auth import auth

    app.register_blueprint(auth,url_prefix='/auth')

    return app
