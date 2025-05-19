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

# Creation d'une fonction pour rechercher un prompt___
def recherche_prompt(mot_cle):
    # connexion a la base de donnée 
    conn = get_db()
    cursor = conn.cursor()

    sql = """
 SELECT prompt.titre, prompt.prix, prompt.note_moyenne,prompt.date_created, 
    date_edited, users.nom 
    FROM prompt 
    JOIN users ON users.id = prompt.author WHERE prompt.etat = 'actif' 
    AND prompt.titre ILIKE %s """

    mot_cle = f"%{mot_cle}%"
    cursor.execute(sql,(mot_cle,))
    data = cursor.fetchall()

    promptes_liste = []

    for p in data:
        prompt_dict = {
            "titre": p[0],
            "prix":p[1],
            "note_moyenne" : p[2],
            "date_created" : p[3],
            "date_edited": p[4],
            "nom_author" : p[5]
        }
        promptes_liste.append(prompt_dict)
    return jsonify(promptes_liste)


# Acheter un prompt 
def acheter_prompt(nom_acheteur, prenom_acheteur, prompt_id):

    # verification des parametres 
    if not nom_acheteur or not prenom_acheteur or not prompt_id:
        return jsonify({"erreur": "Les champs nom_acheteur,prenom \
                       acheteur et le prompt dont obligatoires"}), 400
    
     # connexion a la base de donnée 
    conn = get_db()
    # creation de curseur 
    cursor = conn.cursor()

    try: 
        cursor.execute("""INSERT into achat \
                       (nom_acheteur, prenom_acheteur, prompt_id)\
                       VALUES(%s, %s, %s) RETURNING  id, date_acheter, prix_acheter;""", (nom_acheteur, prenom_acheteur, prompt_id))
        achat = cursor.fetchone()
        conn.commit

        return jsonify({
            "message": "Achat effectué avec succès",
             "achat_id": achat[0],
            "date_acheter": achat[1],
            "prix_acheter": float(achat[2])
        }), 201  
    
    except Exception as e : 
        conn.rollback()
        return jsonify({"erreur": f"l\' erreur est {str(e)}"})
    
    finally:
        cursor.close()
        conn.close()

# Afficher les prompts achetées 
def get_prompt_acheter():

    conn = get_db()
    cursor = conn.cursor()

    sql = """
    SELECT a.id, a.nom_acheteur, \
        a.prenom_acheteur, a.date_acheter,p.titre, \
        a.prix_acheter from achat \
            as a JOIN prompt as p ON a.prompt_id = p.id;"""

    cursor.execute(sql)

    data = cursor.fetchall()

    prompts_lists = []

    for p in data: 
        prompts_dicts = {
            "nom acheteur" : p[0],
            "prenom acheteur": p[1],
            "date achatée" : p[2],
            "titre" : p[3],
            "prix" : p[4]
        } 
        prompts_lists.append(prompts_dicts) 
    return jsonify(prompts_lists)     
    


# # Nous allons rechercher les prompts par des filtres 
# def _recherche_prompt(filtres):

#     # Connexion à la base de donnée 
#     conn = get_db()

#     #creation du curseur 
#     cursor = conn.cursor()
    
#     # La requete sql 

#     requete = """
#     SELECT prompt.titre, prompt.prix, prompt.note_moyenne,prompt.date_created, 
#     date_edited, users.nom 
#     FROM prompt 
#     JOIN users ON users.id = prompt.author WHERE ;
#     """
#     # Conditions initial de notre filtre

#     conditions = ["prompt.etat='actif'"]
    
#     # Les conditions 
#     if mot_cle in filtres:
#         ...

        