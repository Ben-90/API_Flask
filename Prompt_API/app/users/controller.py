from app.db import get_db

def inserer_prompt(data):
    conn = get_db()
    cursor = conn.cursor()

    requete = """
    INSERT INTO prompt (titre, prix, etat, note_moyenne, author)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(requete, (
            data['titre'], 
            data['prix'], 
            data['etat'], 
            data['note_moyenne'], 
            data['author']
        ))
        conn.commit()
        return {"success": True, "message": "Le prompt a été bien enregistré."}
    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}
    finally:
        cursor.close()
        conn.close()
