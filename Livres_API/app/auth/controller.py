import psycopg2
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

def register_user(request):
    data = request.get_json()
    
    # Vérification des données d'entrée
    if not data.get('nom') or not data.get('pwd'):
        return jsonify({"msg": "Nom et mot de passe requis"}), 400

    # Hash du mot de passe
    hashed_pwd = generate_password_hash(data['pwd'], method='sha256')

    # Insertion dans la base de données
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (nom, pwd, id_groupe) VALUES (%s, %s, %s) RETURNING id",
        (data['nom'], hashed_pwd, 1)  # Utiliser id_groupe = 1 pour le groupe par défaut
    )
    user_id = cursor.fetchone()[0]
    db.commit()

    return jsonify({"msg": f"Utilisateur {data['nom']} créé avec succès", "user_id": user_id}), 201

def login_user(request):
    data = request.get_json()

    # Vérification des données d'entrée
    if not data.get('nom') or not data.get('pwd'):
        return jsonify({"msg": "Nom et mot de passe requis"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, pwd FROM users WHERE nom = %s", (data['nom'],))
    user = cursor.fetchone()

    if user and check_password_hash(user[1], data['pwd']):
        # Création du JWT
        access_token = create_access_token(identity=user[0])
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Nom d'utilisateur ou mot de passe incorrect"}), 401
