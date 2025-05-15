from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from .db import init_db

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['DB_URL'] = os.getenv('DB_URL')

    JWTManager(app)
    init_db(app)

    # Importer les blueprints
    from app.books.routes import books_bp
    app.register_blueprint(books_bp, url_prefix="/books")

    # import le blueprint pour auth 
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix = "/auth")

    return app
