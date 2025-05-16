from flask import Blueprint, jsonify, request 
from flask_jwt_extended import jwt_required, get_jwt_identity
from .controller import (list_all_prompts,
                         creer_groupe,creer_user,
                           supprimer_prompt,validation, request_change)

from app.verification_admin_users import admin_verification

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.before_request
@jwt_required()
def check_user():
    user_id = get_jwt_identity()
    if not admin_verification(user_id):
        return jsonify({"message":"Juste les utilisateurs ont une autorisation"})
    

# affichages des prompts 
@admin_bp.route('/prompts', methods=['GET'])
def afficher_les_promptes():
    return jsonify(list_all_prompts())

# validation par 'aldministrateur 
@admin_bp.route('/prompts/<int:prompt_id>/validate', methods=['POST'])
def valider(prompt_id):
    return jsonify(validation(prompt_id))

# Creation des groupes 
@admin_bp.route('/group', methods=['POST'])
def new_groupe():
    data = request.get_json()
    return jsonify(creer_groupe(data)), 201

# Creation des users 
@admin_bp.route('/new_user', methods=['POST'])
def create_new_user():
    data = request.get_json()
    return jsonify(creer_user(data)), 201


# Suppression des prompts 
@admin_bp.route('/prompts/<int:prompt_id>/delete', methods = ['POST'])
def delete_prompt(prompt_id):
    return jsonify(supprimer_prompt(prompt_id))

# Demande de modification 
@admin_bp.route('/prompts/<int:prompt_id>/demande_de_modification', methods=['POST'])
def modifier(prompt_id):
    return jsonify(request_change(prompt_id))

