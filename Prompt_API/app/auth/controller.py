from flask import jsonify, request 
import psycopg2
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

def register_user(request):
    data = request.get_json()

    # Verification si les champs sont remplies 
    if not data.get('nom') or not data.get('pwd'):
        return jsonify({"message": "Veuillez remplir les champs"})
    
    # Hash du mot de passe
    hashed_pwd = generate_password_hash(data['pwd'], method='pbkdf2:sha256')

    # Miantenant nous allons faire la connexion a la base de donnée 
    conn = get_db()
    cursor = conn.cursor()

    # Nous allons à present, faire une insertion à la base de donnée 
    try:
        cursor.execute(
          "INSERT INTO users (nom, pwd, id_groupe) VALUES (%s, %s, %s) RETURNING id",
            (data['nom'], hashed_pwd, 1)
        )
        user_id = cursor.fetchone()[0]
        conn.commit() # On utilise ce commit pour l'enregistrement
        return jsonify({"message" : f"L'utilisateur {data['nom']} à été créé et son id est {user_id}"})
    
    except Exception as e:
        conn.rollback() # ici on utilise un rollback, pouur annuler toute modification s'il y a des erreurs
        print("Erreur lors de la modification", e)
        return jsonify({"Erreur":"Erreur du serveur"})
    
    finally:
        cursor.close() # fermeture de notre cursor 
    

def login(request):
    data = request.get_json()

    #  On va verifier si les champs soont remplis
    if not data.get('nom') or not data.get('pwd'):
        return jsonify({"message": "veuillez rempir les données"})
    
    # Connection a la base de donnée 
    conn = get_db()
    # Creation du curseur 
    cursor = conn.cursor()
    cursor.execute("SELECT id, pwd FROM users WHERE nom = %s", (data['nom'],))
    # Mainternant on stoque la ligne trouvé dans user 
    user = cursor.fetchone()

    if user and check_password_hash(user[1], data['pwd']):
        # Création du JWT
        access_token = create_access_token(identity=str(user[0]))
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Nom d'utilisateur ou mot de passe incorrect"}), 401
