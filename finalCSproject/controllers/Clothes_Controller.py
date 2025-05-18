from flask import Blueprint, render_template, request, redirect, url_for
from models.Clothes_Model import Clothes_Model

clothes_bp = Blueprint('clothes', __name__, template_folder='../templates/clothes')

@clothes_bp.route('/', methods=['GET'])
def list_clothes():
    clothes = Clothes_Model.get_all()
    return render_template('clothes_list.html', clothes=clothes)

@clothes_bp.route('/new', methods=['GET', 'POST'])
def create_clothes():
    if request.method == 'POST':
        clothes_info = {
            'name': request.form['name'],
            'type': request.form['type'],
            'photo': request.files['photo'].read() if 'photo' in request.files else None
        }
        Clothes_Model.create(clothes_info)
        return redirect(url_for('clothes.list_clothes'))
    return render_template('clothes_new.html')

@clothes_bp.route('/<int:id>', methods=['GET'])
def get_clothes(id):
    clothes = Clothes_Model.get(id)
    if not clothes:
        return "Not Found", 404
    return render_template('clothes_detail.html', clothes=clothes)

@clothes_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_clothes(id):
    clothes = Clothes_Model.get(id)
    if not clothes:
        return "Not Found", 404
    if request.method == 'POST':
        clothes_info = {
            'id': id,
            'name': request.form['name'],
            'type': request.form['type'],
            'photo': request.files['photo'].read() if 'photo' in request.files else clothes['photo']
        }
        Clothes_Model.update(clothes_info)
        return redirect(url_for('clothes.get_clothes', id=id))
    return render_template('clothes_edit.html', clothes=clothes)

@clothes_bp.route('/delete/<int:id>', methods=['POST'])
def delete_clothes(id):
    Clothes_Model.remove(id)
    return redirect(url_for('clothes.list_clothes'))
