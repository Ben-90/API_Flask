from flask import Blueprint, request, jsonify
from .controller import affiche_prompts, recherche_prompt, acheter_prompt

# definition des blueprint (les liens)

prompts_bp = Blueprint('prompts', __name__)

# la route, pour afficher tous les prompts 

@prompts_bp.route('/', methods=['GET'])
def get_prompt():
    return affiche_prompts()

# notre route pour faire des recherche sur un mot clé ou le contenue 
@prompts_bp.route('/recherche', methods=['POST'])
def get_recherche():
    data = request.get_json()
    mot_recherche = data.get('mot_cle', '')
    return recherche_prompt(mot_recherche)

# route pour faire un achat d'un prompt 
@prompts_bp.route('/acheter', methods=['POST'])
def faire_un_achat():
     # Récupération des données JSON envoyées par l’utilisateur
    data = request.get_json()

    nom = data.get('nom_acheteur')
    prenom = data.get('prenom_acheteur')
    prompt_id = data.get('prompt_id')

    return acheter_prompt(nom, prenom, prompt_id)