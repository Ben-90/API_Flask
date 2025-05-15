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

    #importer les blueprints pour les prompts 
    from app.prompts.routes import prompts_bp
    app.register_blueprint(prompts_bp, url_prefix="/prompts")

    return app