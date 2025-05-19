from flask import Blueprint, render_template, request, redirect, url_for
from models.Posts_Model import Posts_Model
import base64
import datetime

posts_bp = Blueprint('posts', __name__, template_folder='../templates/posts')

# Initialize the DB
Posts_Model.initialize_DB('models/closetappDB.db')

@posts_bp.route('/posts', methods=['GET'])
def list_posts():
    posts = Posts_Model.get_all()
    for post in posts:
        if post['image']:
            post['image'] = base64.b64encode(post['image']).decode('utf-8')
    return render_template('posts/posts_list.html', posts=posts)

@posts_bp.route('/posts/new', methods=['GET'])
def new_post():
    return render_template('posts/posts_new.html')

@posts_bp.route('/posts', methods=['POST'])
def create_post():
    user_id = int(request.form['user_id'])
    text_content = request.form['text_content']
    visibility = request.form['visibility']
    image_file = request.files['image']
    image_data = image_file.read() if image_file else None

    post_data = {
        'user_id': user_id,
        'text_content': text_content,
        'image': image_data,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'visibility': visibility
    }
    post = Posts_Model.create(post_data)
    return redirect(url_for('home', post_id=post['id']))

@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
def view_post(post_id):
    post = Posts_Model.get_post(post_id)
    if post and post['image']:
        post['image'] = base64.b64encode(post['image']).decode('utf-8')
    print(post, type(post), "viewpost")
    return render_template('posts/posts_view.html', post=post)

@posts_bp.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Posts_Model.get_post(post_id)
    print("edit post,", post_id)
    if request.method == 'POST':
        image_file = request.files['image']
        image_data = image_file.read() if image_file else None
        updated_post_info = {
            'id': post_id,
            'text_content': request.form['text_content'],
            'image': image_data,
            'visibility': request.form['visibility']
        }
        Posts_Model.update(updated_post_info)
        # print("edit post, new post id,", post["id"])
        return redirect(url_for('posts.list_posts'))
    return render_template('posts/posts_edit.html', post=post)

# @posts_bp.route('/posts/<int:post_id>', methods=['POST'])
# def update_post(post_id):
#     post = Posts_Model.get_post(post_id)
#     if not post:
#         return "Post not found", 404

#     text_content = request.form['text_content']
#     visibility = request.form['visibility']
#     image_file = request.files['image']
#     image_data = image_file.read() if image_file and image_file.filename else post['image']

#     updated_data = {
#         'id': post_id,
#         'user_id': post['user_id'],
#         'text_content': text_content,
#         'image': image_data,
#         'created_at': post['created_at'],
#         'updated_at': datetime.datetime.now().isoformat(),
#         'visibility': visibility
#     }

#     Posts_Model.delete(post_id)
#     Posts_Model.create(updated_data)  # Re-create to simulate an update
#     return redirect(url_for('posts.view_post', post_id=post_id))

@posts_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    Posts_Model.delete(post_id)
    return redirect(url_for('posts.list_posts'))
