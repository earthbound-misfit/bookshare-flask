from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

# Add book to bookshelf
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

# Get all books on bookshelf
@api.route('/bookshelf', methods = ['GET'])
@token_required
def get_books(current_user_token):
  this_user = current_user_token.token
  books = Book.query.filter_by(user_token = this_user).all()
  response = books_schema.dump(books)
  return jsonify(response)

# Get book by ID
@api.route('/bookshelf/<id>', methods = ['GET'])
@token_required
def get_book_by_id(current_user_token, id):
  book = Book.query.get(id)
  response = book_schema.dump(book)
  return jsonify(response)

# Update book info
@api.route('/bookshelf/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
  book = Book.query.get(id) 
  book.title = request.json['title']
  book.author = request.json['author']
  book.isbn = request.json['isbn']
  book.pages = request.json['pages']
  book.user_token = current_user_token.token

  db.session.commit()
  response = book_schema.dump(book)
  return jsonify(response)

# Delete book from bookshelf
@api.route('/bookshelf/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
  book = Book.query.get(id)
  db.session.delete(book)
  db.session.commit()
  response = book_schema.dump(book)
  return jsonify(response)