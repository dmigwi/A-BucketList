#!flask/bin/python
from datetime import datetime
from flask import Flask, jsonify, request, make_response, g
from app.models import Item, db, User, BucketList
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
from app.help import help_text, help_message

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

jwt = JWT(app.config['SECRET_KEY'], expires_in=3600)
ACCEPTED_INPUT_FORMAT = ('Accepted input format is {\'name\': \'Name 1\'}')

db.init_app(app)
app.app_context().push()

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


# ======================================
# Operations dealing with error handlers
@app.errorhandler(404)
def handle_error(error):
    return make_response(jsonify({
        'Error': 'Resource Not available, Confirm the URL'}), 404)


@app.errorhandler(401)
def handle_error(error):
    return make_response(jsonify({
        'Error': 'Login failed: Unauthorized access'}), 401)


@app.errorhandler(405)
def handle_error(error):
    return make_response(jsonify({
        'Error': ('%s Method used to access the Resource '
                  'is Invalid' % request.method)}), 405)

# ======================================
# Routes


@app.route('/', methods=['GET'])
def index():
    '''Documentation display'''
    return return_response({'Message': help_message}, 200)


@app.route('/api/v1', methods=['GET'])
def homepage():
    '''Homepage'''
    return return_response({'Message': ('Hello, World!,'
                                        ' This is the Home page')}, 200)


@app.route('/api/v1/auth/login', methods=['POST'])
def auth_login():
    '''Route for logging in'''
    username, password = get_request_data(request)
    user_found = User.query.filter_by(username=username).first()
    if not user_found:
        return return_response(dict(
            Error='Login failed: Unauthorized access'), 401)
    user_found = user_found.get()
    if check_password_hash(user_found.get('password', ''), password):
        return return_response(dict(
            Authorization='Bearer %s' % generate_a_token(user_found)), 201)
    return return_response(dict(
        Error='Login failed: Unauthorized access'), 401)


@app.route('/api/v1/auth/register', methods=['POST'])
def auth_register():
    '''Route for registering'''
    time_now = datetime.now()
    username, password = get_request_data(request)
    if not username or not password:
        return return_response(dict(
            Error='Your password or username is empty or wasn\'t found'), 400)

    user_found = User.query.filter_by(username=username).first()
    if not user_found:
        pw_hash = generate_password_hash(password=password)
        save_user = User(username=username,
                         date_created=time_now,
                         date_modified=time_now,
                         password=pw_hash)
        save_user.save()
        return return_response(dict(Message='Registration Successful'), 201)
    return return_response(dict(Error='Username already exist'), 400)


@app.route('/api/v1/bucketlists', methods=['POST', 'GET'])
@multi_auth.login_required
def bucketlists():
    '''Route for bucketlist(POST) and (GET)'''
    time_now = datetime.now()
    if request.method == 'POST':
        bucklist_name = None
        if request.json:
            bucklist_name = request.json.get('name', None)

        if not bucklist_name:
            return return_response(dict(Error='Create Failed: %s'
                                              '' % ACCEPTED_INPUT_FORMAT), 400)

        all_current_bucketlist = BucketList.query.filter_by(
            created_by=g.user_id).all()
        bucketlist_names = [bucket.name for bucket in all_current_bucketlist]

        # check if the name was passed or exists
        new_items = None
        if bucklist_name not in bucketlist_names:
            b_list = BucketList(name=bucklist_name,
                                date_created=time_now,
                                date_modified=time_now,
                                created_by=g.user_id)
            new_items = b_list.save()

        if new_items:
            return return_response(new_items.get(), 201)
        return return_response(dict(Message="Resource Created Successfully"),
                               201)

    if request.method == 'GET':
        return_bucketlists = {}

        limit = '20' if not request.args else request.args.get('limit', '20')
        limit = 20 if not limit.isdigit() else int(limit)
        if limit > 100:
            return return_response(
                dict(Error=('Get Failed: Only a maximum of 100 '
                            'items can be retrieved at ago')), 400)

        page = '1' if not request.args else request.args.get('page', '1')
        page = 1 if not page.isdigit() else int(page)  # equal to 1 by default

        # Pagination
        count = limit * (page - 1)
        base_query = (BucketList.query.filter_by(created_by=g.user_id).
                      order_by(BucketList.id))
        all_bucks = base_query.paginate(page, limit, False).items

        # searching a word in bucketlist names
        q = '' if not request.args else request.args.get('q', None)
        if q:
            base_query = BucketList.query.filter(BucketList.name.contains(q))
            all_bucks = base_query.filter_by(created_by=g.user_id).all()

        if not all_bucks:
            return return_response(
                dict(Error=('Get Failed: No Bucketlists Found.')), 400)

        for bucket_l in all_bucks:
            items = Item.query.filter_by(bucketlist_id=bucket_l.id).all()
            bucketlists = bucket_l.get()
            bucketlists['item'] = Item().get_all(items)
            count += 1
            return_bucketlists[count] = bucketlists
        return return_response(return_bucketlists, 200)


@app.route('/api/v1/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@multi_auth.login_required
def bucketlists_id(id):
    query = BucketList.query.filter_by(id=id, created_by=g.user_id).first()
    if request.method == 'GET':
        if not query:
            return return_response(dict(
                Error='Get Failed: Bucketlist Id %s was not found' % id), 400)
        query = query.get()

        query_items = Item.query.filter_by(bucketlist_id=id).all()
        query['item'] = Item().get_all(query_items)
        return return_response(query, 200)

    if request.method == 'PUT':
        time_now = datetime.now()
        if not query:
            return make_response(jsonify(dict(
                Error='Update Failed: Bucketlist Id %s '
                'was not found' % id)), 400)

        name = request.json.get('name', None)
        if not name:
            return return_response(dict(Error='Create Failed: %s'
                                              '' % ACCEPTED_INPUT_FORMAT), 400)
        query.name = name
        query.date_modified = time_now
        new_query = query.update()
        return return_response(new_query.get(), 201)

    if request.method == 'DELETE':
        if not query:
            return return_response(dict(
                Error='Delete Failed: Bucketlist Id %s '
                'was not found' % id), 400)
        query.delete()

        query_items = Item.query.filter_by(bucketlist_id=id).all()
        for query_i in query_items:
            query_i.delete()
        return make_response(jsonify({}), 204)


@app.route('/api/v1/bucketlists/<int:id>/items', methods=['POST'])
@multi_auth.login_required
def bucketlists_id_items(id):
    ret_value = request.json

    n_item_name = '' if not ret_value else ret_value.get('name', None)
    if not n_item_name:
        return return_response(dict(Error='Create Failed: %s'
                                    '' % ACCEPTED_INPUT_FORMAT), 400)

    available_bucketlist = BucketList.query.filter_by(id=id,
                                                      created_by=g.user_id
                                                      ).first()
    time_now = datetime.now()
    if not available_bucketlist:
        return return_response(dict(Error='Create Failed: Bucketlist Id'
                                    ' %s was not found' % id), 400)

    available_bucketlist.date_modified = time_now
    available_bucketlist.save()

    query_items = Item.query.all()
    item_names = [item.name for item in query_items]

    # Helps not save a name already saved
    if n_item_name not in item_names:
        item = Item(name=n_item_name)
        item.date_created = time_now
        item.date_modified = time_now
        item.bucketlist_id = available_bucketlist.id
        query_new = item.save()

    if query_new:
        return return_response(query_new.get(), 201)
    return return_response(dict(Message="Resource already exists"), 201)


@app.route('/api/v1/bucketlists/<int:id>/items/<int:item_id>',
           methods=['PUT', 'DELETE'])
@multi_auth.login_required
def bucketlist_id_items_item_id(id, item_id):
    # Route for deleting and editing the item
    if request.method == 'PUT':
        time_now = datetime.now()
        query_bucketList = BucketList.query.filter_by(id=id,
                                                      created_by=g.user_id
                                                      ).first()
        query_items = Item.query.filter_by(bucketlist_id=id,
                                           id=item_id).first()
        if not query_items or not query_bucketList:
            return return_response(dict(Error='Update Failed: '
                                        'You provided Item Id or BucketList'
                                        ' Id that is non existent '), 400)

        item_name = request.json.get('name', '')
        item_done = request.json.get('done', False)

        # Ensures that only boolean True is passed if not boolean False
        item_done = True if str(item_done).lower() == 'true' else False

        if not item_name:
            return return_response(dict(Error='Update Failed: Item Name was'
                                        ' not found'), 400)

        query_items.name = item_name
        query_items.date_modified = time_now
        query_items.done = item_done
        query_items.update()

        query_bucketList.date_modified = time_now
        query_bucketList.update()

        query_updated_item = Item.query.filter_by(
            date_modified=time_now, id=query_items.id).first()
        if query_updated_item:
            return return_response(query_updated_item.get(), 201)
        return return_response(
            dict(Message="Resource Updated Successfully"), 201)

    if request.method == 'DELETE':
        query_items = Item.query.filter_by(
            bucketlist_id=id, id=item_id).first()
        if not query_items:
            return return_response(
                dict(Error='Deleted Failed: You provided Item Id or'
                           ' BucketList Id that is non existent'), 400)
        query_items.delete()
        return return_response({}, 204)


# ======================================
#  username and password verification
@basic_auth.verify_password
def verify_password(username, password):
    user_details = User.query.filter_by(username=username).first()
    g.user_id = 0
    if user_details and check_password_hash(
            user_details.password, password):
        g.user_id = user_details.id
        return True
    return False


# ======================================
# Token Authentication
@token_auth.verify_token
def verify_token(token):
    g.user_id = 0
    try:
        data = jwt.loads(token)['username']
    except:
        return False
    users = User.query.filter_by(username=data.get('username', '')).first()
    if users.id == data['id']:
        g.user_id = users.id
        return True
    return False


# ======================================
# Helper functions
def generate_a_token(user):
    JWT(app.config['SECRET_KEY'], expires_in=3600)
    token = jwt.dumps({'username': user})
    return token.decode(encoding="utf-8")


def return_response(message, code):
    return jsonify(message), code


def get_bucketlist(id, operation):
    query = BucketList.query.filter_by(id=id, created_by=g.user_id).first()
    if not query:
        return return_response(dict(
            Error=('%s Failed: Bucketlist Id %s '
                   'was not found' % (id, operation))), 400)
    return query


# ======================================
# Method to check if databases exit and return help message if otherwise
@app.before_request
def dbs_exist():
    '''Method provides a help text if the tables don\'t exist'''
    engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    user_table = engine.dialect.has_table(engine, 'user')
    bucketlist_table = engine.dialect.has_table(engine, 'bucketlist')
    items_table = engine.dialect.has_table(engine, 'items')

    # This is a server side error because not tables were found
    if not user_table or not bucketlist_table or not items_table:
        # during testing do not return the error message
        if app.config['ENV'] != 'testing':
            return return_response(help_text, 500)


# ======================================
# Method to help retrieve data from password fields
def get_request_data(request):
    form_d = request.form
    json_d = request.json

    # Check if not password or username passed
    if not form_d and not json_d:
        return ('', '')

    username = (form_d.get('username', '') if form_d
                else json_d.get('username', ''))
    password = (form_d.get('password', '') if form_d
                else json_d.get('password', ''))

    return (username, password)
