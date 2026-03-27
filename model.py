from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#User model for the database
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    userType = db.Column(db.String, nullable=False)

    def __repr__(self): 
        return f'<User {self.fullname}>' #This is a special method that defines how the User object is represented as a string, which can be useful for debugging and logging purposes.

# class Products(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
    
