from app.db import get_db

# Creation des fonctions 

# lister tous les prompts 

def list_all_prompts():

    # Connexion à la base de donnée 
    conn = get_db()
    
    # Creation du cursor 
    cur = conn.cursor()

    sql = """
SELECT p.id, p.titre, p.prix, p.etat, 
p.date_created, p.date_edited,
p.note_moyenne, u.nom FROM prompt as p JOIN users as u ON p.author = u.id; """
    
    # On recupere les prompts 
    cur.execute(sql)
    rows = cur.fetchall()
    
    cur.close()

    # afficher les elements 

    return [
        {"id":row[0], 
         "titre": row[1], 
         "prix": row[2], 
         "etat": row[3], 
         "date_created":row[4],
           "date_edited":row[5], 
           "note_moyenne":row[6], 
           "nom": row[7]} 

           for row in rows

           ]


# Creer des users

def creer_user(data):
    
    # connexion à la base de donnée 
    conn = get_db()
    #Creation du curseur 
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (nom, pwd, id_groupe) VALUES (%s, %s, %s)",
            (data["nom"], data["pwd"], data["id_groupe"])
        )
        conn.commit()
        return {"success": True, "message":"L'utilisateur est bien creer."}
    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}
    finally: 
        conn.close()

# Creation des groupes 

def creer_groupe(data):

    # Connexion à la base de donnée 

    conn = get_db()
    # creation du curosr 
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO groupe (nom) VALUES (%s)", (data["nom"],)
        )
        conn.commit()
        return {"success": True, "message": "Groupe creer"}
    except Exception as e: 
        conn.rollback()
        return {"success": False, "message": str(e)}
    finally:
        conn.close()
    
# Creation d'une fonction pour supprimer 

def supprimer_prompt(promp_id):
    # connexion a la base de donnée 
    conn = get_db()
    # creation du cursor 
    cur = conn.cursor()

    sql = """
DELETE FROM prompt WHERE id = %s"""
    try: 
        cur.execute(sql, (promp_id,))
        conn.commit()
        return {"success": True, "message": f"Le prompt {promp_id} a ete bien supprime"}
    except Exception as e:
        conn.rollback()
        return {"suceess": False, "error": str(e)}
    finally:
        cur.close()
        conn.close()


# Fonction de changement d'etat 
# Cette fonction, on va l'utiliser a l'interieur de chaque fonction 

def _changement_etat(prompt_id, nouvelle_etat):

    # connexion à la base de donnée 

    conn = get_db()
    
    # creation du curseur 

    cursor = conn.cursor()

    # Changement à la base de donnée 
    try : 
        cursor.execute("UPDATE prompt SET etat= %s WHERE id = %s", (nouvelle_etat, prompt_id))
        conn.commit()
        return {"success": True, "message": f"Le prompt {prompt_id} est mis a jour a {nouvelle_etat}"}

    except Exception as e : 
        conn.rollback()
        return {"success": False, "message": str(e)}

    finally: 
        conn.close()    


# Fonction de validation 

def validation(prompt_id):
    return _changement_etat(prompt_id, 'actif')

# demande de modification 

def request_change(prompt_id):
    return _changement_etat(prompt_id, 'a revoir')

