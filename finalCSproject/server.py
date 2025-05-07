from flask import Flask
from controllers.User_Controller import user_routes

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(user_routes, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
