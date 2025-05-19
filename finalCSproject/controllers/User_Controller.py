from flask import Blueprint, render_template, request, redirect, url_for
from models.User_Model import User_Model

user_routes = Blueprint('user_routes', __name__, template_folder='../templates/user')

@user_routes.route('/', endpoint='index')
def index():
    users = User_Model.get_all()
    return render_template('user/index.html', users=users)

@user_routes.route('/<int:user_id>', endpoint='detail')
def detail(user_id):
    user = User_Model.get(user_id)
    return render_template('user/detail.html', user=user)

@user_routes.route('/create', methods=['GET', 'POST'], endpoint='create')
def create():
    if request.method == 'POST':
        data = {
            "username": request.form['username'],
            "email": request.form['email'],
            "password": request.form['password']
        }
        User_Model.create(data)
        return redirect(url_for('login'))
    return render_template('user/create.html')

@user_routes.route('/<int:user_id>/edit', methods=['GET', 'POST'], endpoint='edit')
def edit(user_id):
    user = User_Model.get(user_id)
    if request.method == 'POST':
        updated = {
            "id": user_id,
            "username": request.form['username'],
            "email": request.form['email'],
            "password": request.form['password']
        }
        User_Model.update(updated)
        return redirect(url_for('home'))
    return render_template('user/edit.html', user=user)

@user_routes.route('/users/delete/<string:username>', methods=['POST'])
def delete_user(username):
    # Optional: Only allow deletion if logged-in user matches or is admin
    User_Model.remove(username)
    return redirect(url_for('logout'))  # Or homepage
