from flask import Blueprint, jsonify
from .controller import get_all_books

# Définir le blueprint
books_bp = Blueprint('books', __name__)

# La route pour afficher tous les livres
@books_bp.route('/', methods=['GET'])
def get_books():
    return get_all_books()  # Appel à la fonction dans controller.py
