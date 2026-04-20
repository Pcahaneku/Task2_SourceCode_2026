from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#User model for the database
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50))

    def __repr__(self): 
        return f'<User {self.fullname}>' #This is a special method that defines how the User object is represented as a string, which can be useful for debugging and logging purposes.

#Product model for the database
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False) #Stores Image as a Binary
    filename = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.Text(500))

#Order model for the database
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
