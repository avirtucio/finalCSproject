from flask import Blueprint, render_template, request, redirect, url_for
from models.Closets_Model import Closets_Model
import os

closets_bp = Blueprint('closets_bp', __name__, template_folder='../templates/closets')

DB_PATH = os.path.join(os.path.dirname(__file__), '../closetappDB.db')

@closets_bp.route('/closets')
def list_closets():
    closets = Closets_Model.get_all()
    return render_template('closets_list.html', closets=closets)

@closets_bp.route('/closets/<int:user_id>')
def user_closet(user_id):
    closet = Closets_Model.get_user_closet(user_id)
    if closet:
        return render_template('closets_detail.html', closet=closet)
    else:
        return "Closet not found", 404

@closets_bp.route('/closets/<int:user_id>/add', methods=['POST'])
def add_item(user_id):
    clothes_id = request.form.get('clothes_id')
    if not clothes_id:
        return "No clothes ID provided", 400

    updated_closet = Closets_Model.add_item(user_id, int(clothes_id))
    return redirect(url_for('closets_bp.user_closet', user_id=user_id))
