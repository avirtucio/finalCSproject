from flask import Flask
from controllers.User_Controller import user_routes
from controllers.Clothes_Controller import clothes_bp
from controllers.Closets_Controller import closets_bp

from models.User_Model import User_Model
from models.Clothes_Model import Clothes_Model
from models.Closets_Model import Closets_Model

import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'closetappDB.db')

import base64

# Register controller blueprints
app = Flask(__name__, static_url_path='/static')
app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(clothes_bp, url_prefix='/clothes')
app.register_blueprint(closets_bp)

def bootstrap_database():
    Clothes_Model.initialize_DB(DB_PATH)
    User_Model.initialize_DB(DB_PATH) 
    Closets_Model.initialize_DB(DB_PATH)
     # Add others like Closet_Model, etc.

bootstrap_database()

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
