from app.db import get_db
def is_user_admin(user_id):

    # connexion a la base de donnée 
    conn = get_db()
    # activation du curseur 
    cur = conn.cursor()
    sql = """
SELECT g.nom FROM groupe as g 
JOIN users as u ON u.id_groupe = g.id_groupe 
WHERE u.id = %s; 
"""
    cur.execute(sql, (user_id,))
    resultat = cur.fetchone()
    cur.close()

    return resultat and resultat[0].lower() == "admin"