from app.db import get_db 

def is_not_admin(user_id):
    # Connexion à la base de données
    conn = get_db()
    cur = conn.cursor()

    sql = """
    SELECT g.nom FROM groupe AS g
    JOIN users AS u ON u.id_groupe = g.id_groupe
    WHERE u.id = %s;
    """
    cur.execute(sql, (user_id,))
    result = cur.fetchone()
    cur.close()

    if result is None:
        # Aucun groupe trouvé pour cet utilisateur : on considère qu’il n’est pas admin
        return True

    # Vérifie si le groupe est différent de "admin"
    return result[0].strip().lower() != "admin"
