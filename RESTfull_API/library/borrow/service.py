from library.extension import db
from library.library_ma import BorrowSchema
from library.model import Borrow, Books, Students, Author, Category
from flask import request, jsonify
from sqlalchemy import func
import json 


def get_borrow_author_cat_service(student_name):
    borrows = db.session.query(Borrow.id, Books.name, Category.name, Author.name).join(Students, 
    Borrow.student_id == Students.id).join(Books, Borrow.book_id == Books.id).join(Category, Books.category_id == Category.id).join(Author, Books.author_id == Author.id).filter(func.lower(Students.name) == func.lower(student_name)).all()
    if borrows:
        return jsonify({f"{student_name} borrowed": borrows}), 200
    else:
        return jsonify({"message": "Not found borrow!"}), 404
