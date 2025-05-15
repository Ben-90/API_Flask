import psycopg2
from flask import g, current_app
import os 
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_db():
    if 'db' not in g:
        try:
            g.db = psycopg2.connect(DATABASE_URL)
        except psycopg2.Error as e:
            print("Erreur lors de la connexion à la base de données : ", e)
            raise e  # Vous pouvez aussi choisir de lever une exception personnalisée si nécessaire
    return g.db

def init_db(app):
    @app.teardown_appcontext
    def close_db(error):
        db = g.pop('db', None)
        if db is not None:
            db.close()
