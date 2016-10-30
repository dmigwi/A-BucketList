#!flask/bin/python
from flask import Flask, abort, jsonify, request, make_response
from app.models import Item, db, User
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'data': 'Hello, World!, This is the Home page'})


@app.route('/auth/login', methods=['POST'])
def auth_login():
    abort(403)


@app.route('/auth/register', methods=['POST'])
def auth_register():
    abort(403)


@app.route('/bucketlists', methods=['POST, GET'])
@auth.login_required
def bucketlists():
    abort(403)


@app.route('/bucketlists/<id>', methods=['GET, PUT, DELETE'])
@auth.login_required
def bucketlists_id():
    abort(403)


@app.route('/bucketlists/<id>/items', methods=['POST'])
@auth.login_required
def bucketlists_id_items():
    abort(403)


@app.route('/bucketlists/<id>/items/<item_id>',
           methods=['PUT, DELETE'])
@auth.login_required
def bucketlist_id_items_item_id():
    abort(403)


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    app.run(debug=True)
