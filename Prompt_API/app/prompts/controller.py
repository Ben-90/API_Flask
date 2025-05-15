from flask import jsonify
from app.db import get_db


# une fonction pour afficher tous les prompts existants 

def affiche_prompts():
    db = get_db()
    cursor = db.cursor()
    sql = """
    SELECT prompt.id,prompt.titre, prompt.prix, prompt.note_moyenne,prompt.date_created, 
    date_edited, users.nom 
    FROM prompt 
    JOIN users ON users.id = prompt.author;
  """
    cursor.execute(sql)
    
    data = cursor.fetchall()

    prompt_list = []

    for p in data:
        prompt_dict = {
            "id": p[0],
            "titre": p[1],
            "prix":p[2],
            "note_moyenne" : p[3],
            "date_created" : p[4],
            "date_edited": p[5],
            "nom_author" : p[6]
        }

        prompt_list.append(prompt_dict)
    return jsonify(prompt_list)
    