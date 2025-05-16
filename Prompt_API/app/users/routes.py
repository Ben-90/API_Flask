from flask import Blueprint, jsonify, request 
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.admin.controller import list_all_prompts
from .controller import inserer_prompt
from app.verification_admin_users.user_verfication import is_not_admin

user_bp = Blueprint("user_bp", __name__)

# Afficher tous les prompts côté utilisateur
@user_bp.route('/prompts', methods=['GET'])
def affiche_prompts():
    return jsonify(list_all_prompts())

# Création d’un prompt
@user_bp.route('/prompts', methods=['POST'])
@jwt_required()
def creer_prompt():
    user_id = int(get_jwt_identity())

    # 🔒 Vérifie si l'utilisateur est admin
    if not is_not_admin(user_id):
        return jsonify({
            "success": False,
            "message": "Les administrateurs ne peuvent pas créer de prompt."
        }), 403

    data = request.get_json()
    data['author'] = user_id

    resultat = inserer_prompt(data)
    return jsonify(resultat), 201 if resultat["success"] else 400