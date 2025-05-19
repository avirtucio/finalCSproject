from flask import Blueprint, render_template, request, redirect, url_for
import json
from models.Outfits_Model import Outfits_Model

outfits_bp = Blueprint('outfits', __name__, template_folder='../templates/outfits')

# Initialize DB on import
Outfits_Model.initialize_DB('models/closetappDB.db')

@outfits_bp.route('/outfits')
def list_outfits():
    outfits = Outfits_Model.get_all()
    return render_template('outfits_list.html', outfits=outfits)

@outfits_bp.route('/outfits/new', methods=['GET', 'POST'])
def create_outfit():
    if request.method == 'POST':
        name = request.form['name']
        user_id = int(request.form['user_id'])
        clothes_list = request.form.getlist('clothes_list')[0].split(",")  # Expecting list of clothes ids from form
        print(clothes_list, type(clothes_list))
        for id in clothes_list:
            print(id)
        clothes_json = json.dumps([int(c) for c in clothes_list])
        outfit_info = {
            'name': name,
            'user_id': user_id,
            'clothes_list': clothes_json
        }
        Outfits_Model.create(outfit_info)
        return redirect(url_for('outfits.list_outfits'))
    return render_template('outfits_create.html')

@outfits_bp.route('/outfits/<int:outfit_id>')
def outfit_detail(outfit_id):
    outfit = Outfits_Model.get_outfit(id=outfit_id)
    print(outfit)
    if outfit:
        # Decode clothes_list JSON string to Python list for template
        outfit['clothes_list'] = json.loads(outfit['clothes_list'])
    # print(outfit_id, "outfit id in outfit_detail", type(outfit_id))
    return render_template('outfits_view.html', outfit=outfit, outfit_id=outfit_id)

@outfits_bp.route('/outfits/delete/<int:outfit_id>', methods=['POST'])
def delete_outfit(outfit_id):
    Outfits_Model.remove(outfit_id)
    return redirect(url_for('outfits.list_outfits'))
