from library.extension import db, ma
from library.library_ma import BooksSchema
from library.model import Books, Author
from flask import request 
from flask import jsonify
from sqlalchemy import func
import json 
book_schema = BooksSchema()
books_schema = BooksSchema(many=True)

def add_book_service():
    data = request.json
    if (data and ('name' in data) and ('page_count' in data)
            and ('author_id' in data) and ('category_id' in data)):
        name = data['name']
        page_count = data['page_count']
        author_id = data['author_id']
        category_id = data['category_id']
        try:
            new_book = Books(name, page_count, author_id, category_id)
            db.session.add(new_book)
            db.session.commit()
            return jsonify({"message": "Add success!"}), 200
        except IndentationError:
            db.session.rollback()
            return jsonify({"message": "Can not add book!"}), 400
    else:
        return jsonify({"message": "Request error"}), 400
    
def get_book_by_id_service(id):
    book = Books.query.get(id)
    if book:
        return book_schema.jsonify(book) 
    else:
        return jsonify({"message": "Book not found"}), 404

def get_all_books_service():
    books = Books.query.all()
    return books_schema.jsonify(books), 200

def update_book_by_id_service(id):
    data = request.json
    book = Books.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    if not data:
        return jsonify({"message": "Request error"}), 400

    if "name" in data:
        book.name = data["name"]
    if "page_count" in data:
        book.page_count = data["page_count"]
    if "author_id" in data:
        book.author_id = data["author_id"]
    if "category_id" in data:
        book.category_id = data["category_id"]
    db.session.commit()
    return jsonify({"message": "Update success!"}), 200

def delete_book_by_id_service(id):
    book = Books.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Delete success!"}), 200
    
def get_book_by_author_service(author):
    books = Books.query.join(Author).filter(func.lower(Author.name) == func.lower(author)).all()
    if books:
        return books_schema.jsonify(books)
    else:
        return jsonify({"message": "No books found for the given author"}), 404
