from flask import Flask, render_template, request, session, redirect, url_for, flash
from model import db, User, Product, Order
from flask_bcrypt import Bcrypt
import os  #This is used to interact with the operating system, such as for file handling or environment variables.

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'avery_long_secret_random_key') #This sets the secret key for the Flask application, which is used for securely signing the session cookie and other security-related needs. It tries to get the value from an environment variable named 'SECRET_KEY', and if that variable is not set, it defaults to 'avery_long_secret_random_key'.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db' #This configures the app to use an SQLite database named 'grocery.db' located in the same directory as the app.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #This disables the SQLAlchemy event system that tracks modifications of objects and emits signals.

db.init_app(app)

with app.app_context():
    db.create_all()

with app.app_context(): 
# PRODUCTS List 
    if not Product.query.first(): #If no products exists in database
            products = [
                Product(name='Fresh Apple 1', description='Apple. Crisp and sweet, perfect for snacking.', price=0.30), 
                Product(name='GLH Medium Cucumbers 250G', description='Cucumber. Carefully selected to be cool and crisp with extra crunch and comes in a medium size.', price=1.80),
                Product(name='GLH Banana Loose 1', description='Banana. Hand picked and ripened with a sweet flavour added to it.', price=0.50),
                Product(name='GLH Cherry Tomatoes 350G', description='Tomatoes. Vine ripened for a crsip bit, with juicy flavour.', price=1.50)
                ]

            db.session.add_all(products)
            db.session.commit()




#HOMEPAGE ROUTE that renders the homepage.html template and leads to the homepage page. 
@app.route('/')
def homepage():
    return render_template ('homepage.html')

#REGISTRATION ROUTE that renders the register.html template and leads to the registration page. 
@app.route('/register', methods=['GET', 'POST']) 
def register():
     
    if request.method == 'POST':

        fullname = request.form.get('fullname')
        email = request.form.get('email')
        plain_password = request.form.get('password')

        #HASHING THE PASSWORD
        hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

        gender = request.form.get("gender")
        role = request.form.get('role')

        role = "customer"

        #VALIDATION
        if not fullname or not email or not plain_password:
            flash('Please fill out all required fields.')
            return render_template('register.html')

        #FIXED EMAIL VALIDATION
        if '@' not in email or '.' not in email:
            flash('Invalid email format', 'error')
            return render_template('register.html')
        if len(plain_password) < 8 or len(plain_password) > 20:
            flash('Password must be 8 - 20 characters', 'error')
            return render_template('register.html')
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already registered', 'error')
            return render_template('register.html')

        # FIXED GENDER VALIDATION
        if gender == 'Other':
            flash('Please select a valid gender.', 'error')
            return render_template('register.html')
        
        
        
        # CREATE A NEW USER INSTANCE    
        new_user = User(
            fullname=fullname, 
            email=email, 
            password=hashed_password, 
            gender=gender,
            role=role
        )

        try: 
            db.session.add(new_user)  
            db.session.commit() #This saves the new user to the database. 
            flash('Registration successful! Please login.', 'success') # If successful, it flashes a success message and redirects the user to the login page.
            return render_template('login.html') #directs users to the Login Page
        except Exception as e:
            return f"An error occured: {e}"

    return render_template('register.html') 

#LOGIN ROUTE that renders the login.html template and leads to the login page. 
@app.route('/login', methods=["GET", "POST"]) 
def login():
     
    if request.method == 'POST':

        email = request.form.get('email')
        plain_password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, plain_password):
            session['user_id'] = user.id #This stores the user's ID in the session, allowing the application to keep track of the logged-in user across different requests.
            session['user_email'] = user.email #This stores the user's email in the session, which can be used for display purposes or other functionalities that require the user's email.

            flash('Login successful', 'success')
            return redirect(url_for('account')) #This redirects the user to the homepage after a successful login.
        
        # Admin Session
        if user:
            session['user_id'] = user.id
            session['user_role'] = user.role
        
        flash('Invalid email or password', 'error') #If the login credentials are incorrect, it flashes an error message and re-renders the login page.
        return redirect(url_for('login'))

    return render_template('login.html') #If the user is logged in, it renders the login.html template.



#ADMIN DASHBOARD ROUTE that renders the admin_dashboard.html template and leads to the admin_dashboard page. 
@app.route('/admin_dashboard') 
def admin_dashboard():

    if 'role' != 'admin':
      flash ('Access Denied')

      return render_template('admin_dashboard.html') #If the admin is logged in, it renders the admin_dashboard.html template.

#ACCOUNT ROUTE that renders the order.html template and leads to the offers page. 
@app.route('/account') 
def account():

    if "user_id" not in session:
        flash("Please Register/Login to access your account")
        return redirect(url_for("login"))

    users = None

    return render_template("account.html", users=users)

#PRODUCTS ROUTE that renders the products.html template and leads to the products page. 
@app.route('/products') 
def products():
        products = Product.query.all()

        return render_template('products.html', product=products) 

#PRODUCT DETAILS 
@app.route('/products/<int:id>')
def product_details(id):
    product = Product.query.get_or_404
    return render_template('product_details.html', product=products)

#ORDERS ROUTE that renders the order.html template and leads to the offers page. 
@app.route('/order') 
def order():
      
    if "user_id" not in session:
        flash("Register/Login to see your Order History")
        return redirect(url_for("login"))

    users = None

    return render_template('order.html', users=users) 

#OFFERS ROUTE that renders the offers.html template and leads to the offers page. 
@app.route('/offers') 
def offers():
      return render_template('offers.html') 

#INFORMATIONS ROUTE that renders the informations.html template and leads to the informations page. 
@app.route('/info')
def info():
     return render_template('info.html')

#PRIVACY ROUTE that renders the privacy.html template and leads to the privacy page. 
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

#CART ROUTE that renders the terms.html template and leads to the terms&conditions page. 
@app.route('/terms')
def terms():
    return render_template('terms.html')

#LOGOUT PAGE that renders the logout.html template and leads to the logout page. 
@app.route('/logout')
def logout():
     
     session.clear() #This clears all data from the session, efficiently logging the user ot by removing their user ID and email form the seesion.

     flash('You have been logged out successfully', 'success')

     return render_template('homepage.html') #This redirects the user to the homepage after logging out.

#This helps in running the app in debug mode. By reloading the server when code changes.
if __name__ == '__main__': 
    app.run(debug=True)

    