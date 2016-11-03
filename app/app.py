#!flask/bin/python
from flask import Flask, abort, jsonify, request, make_response, g
from app.models import Item, db, User
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
from werkzeug.exceptions import MethodNotAllowed

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'confidential top secret!'
jwt = JWT(app.config['SECRET_KEY'], expires_in=3600)

db.init_app(app)

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'data': 'Hello, World!, This is the Home page'})


@app.route('/auth/login', methods=['POST'])
def auth_login():
    return make_response(jsonify({}), 401)


@app.route('/auth/register', methods=['POST'])
def auth_register():
    return make_response(jsonify({}), 401)


@app.route('/bucketlists', methods=['POST', 'GET'])
@multi_auth.login_required
def bucketlists():
    return make_response(jsonify({}), 401)


@app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@multi_auth.login_required
def bucketlists_id(id):
    return make_response(jsonify({}), 401)


@app.route('/bucketlists/<int:id>/items', methods=['POST'])
@multi_auth.login_required
def bucketlists_id_items(id):
    return make_response(jsonify({}), 401)


@app.route('/bucketlists/<int:id>/items/<int:item_id>',
           methods=['PUT', 'DELETE'])
@multi_auth.login_required
def bucketlist_id_items_item_id(id, item_id):
    return make_response(jsonify({}), 401)


users = {'username': 'kgumba', 'password': 'k'}


@basic_auth.verify_password
def verify_password(username, password):
    g.user = None
    if username in users:
        if check_password_hash(users.get(username), password):
            g.user = username
            return True
    return False


@token_auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = jwt.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False


@app.errorhandler(401)
def handle401(e):
    return make_response(jsonify({'Error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    app.run(debug=True)
