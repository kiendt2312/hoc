from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .model import Students, Books, Borrow, Category, Author

class StudentsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Students
        load_instance = True

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True

class BooksSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Books
        load_instance = True

class BorrowSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Borrow
        load_instance = True