from flask import jsonify, Blueprint, request
from .controller import login, register_user

# Creation du blueprint 
auth_bp = Blueprint('auth', __name__)

# Creztion de la route pour enregistrer 
@auth_bp.route('/register', methods=['POST'])
def register():
    return register_user(request)

# Creation de la route pour login 
@auth_bp.route('/login', methods=['POST'])
def login_print():
    return login(request)