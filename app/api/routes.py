from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/bookshelf', methods = ['POST'])
@token_required
def add_book(current_user_token):
  title = request.json['title']
  author = request.json['author']
  isbn = request.json['isbn']
  pages = request.json['pages']
  user_token = current_user_token.token

  book = Book(title, author, isbn, pages, user_token=user_token)

  db.session.add(book)
  db.session.commit()

  response = book_schema.dump(book)
  return jsonify(response)

