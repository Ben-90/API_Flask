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

    #importer les blueprints pour les prompts visiteurs 
    from app.prompts.routes import prompts_bp
    app.register_blueprint(prompts_bp, url_prefix="/prompts")

    # IMportert les blueprints pour l'authentification
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auths")
    
    # Importer les blueprints pour le admin 
    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix = "/admin")

    # Importation des blueprints pour les users
    from app.users.routes import user_bp
    app.register_blueprint(user_bp, url_prefix = "/users")


    return app