from flask import Blueprint, request, jsonify
from .controller import affiche_prompts

# definition des blueprint (les liens)

prompts_bp = Blueprint('prompts', __name__)

# la route, pour afficher tous les prompts 

@prompts_bp.route('/', methods=['GET'])
def get_prompt():
    return affiche_prompts()