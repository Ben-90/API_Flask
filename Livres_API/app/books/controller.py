from flask import jsonify
from app.db import get_db

def get_all_books():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, titre, prix, etat FROM LIVRES WHERE etat = 'actif'")
    books = cursor.fetchall()

    book_list = []
    for book in books:
        book_dict = {
            "id": book[0],
            "titre": book[1],
            "prix": book[2],
            "etat": book[3]
        }
        book_list.append(book_dict)

    return jsonify(book_list), 200
