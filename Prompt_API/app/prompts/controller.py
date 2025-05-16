from flask import jsonify
from app.db import get_db


# une fonction pour afficher tous les prompts existants 

def affiche_prompts():
    db = get_db()
    cursor = db.cursor()
    sql = """
    SELECT prompt.titre, prompt.prix, prompt.note_moyenne,prompt.date_created, 
    date_edited, users.nom 
    FROM prompt 
    JOIN users ON users.id = prompt.author WHERE prompt.etat = 'actif';
  """
    cursor.execute(sql)
    
    data = cursor.fetchall()

    prompt_list = []

    for p in data:
        prompt_dict = {
            "titre": p[0],
            "prix":p[1],
            "note_moyenne" : p[2],
            "date_created" : p[3],
            "date_edited": p[4],
            "nom_author" : p[5]
        }

        prompt_list.append(prompt_dict)
    return jsonify(prompt_list)
    