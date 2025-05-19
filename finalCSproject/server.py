from flask import Flask, render_template, request, redirect, url_for, session
from controllers.User_Controller import user_routes
from controllers.Clothes_Controller import clothes_bp
from controllers.Closets_Controller import closets_bp
from controllers.Outfits_Controller import outfits_bp
from controllers.Posts_Controller import posts_bp

from models.User_Model import User_Model
from models.Clothes_Model import Clothes_Model
from models.Closets_Model import Closets_Model
from models.Outfits_Model import Outfits_Model
from models.Posts_Model import Posts_Model

import os, json, base64
DB_PATH = os.path.join(os.path.dirname(__file__), 'closetappDB.db')

import base64

# Register controller blueprints
app = Flask(__name__, static_url_path='/static')
app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(clothes_bp, url_prefix='/clothes')
app.register_blueprint(closets_bp)
app.register_blueprint(outfits_bp)
app.register_blueprint(posts_bp)

app.secret_key = 'your_secret_key'

def bootstrap_database():
    Clothes_Model.initialize_DB(DB_PATH)
    User_Model.initialize_DB(DB_PATH) 
    Closets_Model.initialize_DB(DB_PATH)
    Outfits_Model.initialize_DB(DB_PATH)
    Posts_Model.initialize_DB(DB_PATH)
     # Add others like Closet_Model, etc.

bootstrap_database()

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

@app.template_filter('fromjson')
def fromjson_filter(s):
    return json.loads(s)

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists and password is correct
        user = User_Model.get(username)
        if user and user['password'] == password:  # Replace with hashed check in production
            session['username'] = username
            session['user_id'] = user['id']
            print("login, username", username)
            return redirect(url_for('home', username=username))  # Replace with actual home endpoint
        else:
            error = 'Invalid username or password.'

    return render_template('login.html', error=error)

@app.route('/profile')
def profile():
    username = session['username']
    user = User_Model.get(username)
    # print("profile", user)
    # You can fetch user data here and pass it to the template
    return render_template('profile.html', user=user)

@app.route('/closet')
def closet():
    username = session['username']
    user = User_Model.get(username)
    # print("profile", user)
    # Fetch closet-related data and pass it to the template
    return render_template('closet.html', user=user)

@app.route('/stylist')
def stylist():
    username = session['username']
    user = User_Model.get(username)
    user_closet = Closets_Model.get_user_closet(user["id"])["clothes_list"]
    closet_items = []
    for clothes_id in user_closet:
        closet_items.append(Clothes_Model.get(clothes_id))
    # print("profile", user)
    # Fetch stylist-related data and pass it to the template
    print("stylist,", user["id"])
    outfits = Outfits_Model.get_all_user_outfits(user_id=int(user["id"]))
    return render_template('stylist.html', user=user, closet_items=closet_items, outfits=outfits)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username').strip()
#         email = request.form.get('email').strip()
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirm_password')

#         # Basic validation
#         if not username or not email or not password or not confirm_password:
#             error = "Please fill out all fields."
#             return render_template('register.html', error=error)

#         if password != confirm_password:
#             error = "Passwords do not match."
#             return render_template('register.html', error=error)

#         # TODO: Check if username or email already exists in your DB
#         # Example (replace with your DB query):
#         # if User.exists(username=username):
#         #     error = "Username already taken."
#         #     return render_template('register.html', error=error)
#         # if User.exists(email=email):
#         #     error = "Email already registered."
#         #     return render_template('register.html', error=error)

#         # Hash the password
#         hashed_password = generate_password_hash(password)

#         # TODO: Save the user to the database
#         # Example:
#         # new_user = User(username=username, email=email, password=hashed_password)
#         # new_user.save()

#         # After successful registration, redirect to login or home page
#         flash("Registration successful! Please log in.")
#         return redirect(url_for('login'))

#     # GET request — just show the registration form
#     return render_template('register.html')

# Example route for home
@app.route('/home')
def home():
    username = session['username']
    user = User_Model.get(username)
    posts = Posts_Model.get_all()
    for post in posts:
        if post['image']:
            post['image'] = base64.b64encode(post['image']).decode('utf-8')
    # return render_template('home.html', username=username)
    return render_template('home.html', username=session.get('username'), user=user, posts=posts)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
