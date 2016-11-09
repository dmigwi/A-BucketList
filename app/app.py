#!flask/bin/python
from datetime import datetime
from flask import Flask, jsonify, request, make_response, g
from app.models import Item, db, User, BucketList
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
# import logging as log

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

jwt = JWT(app.config['SECRET_KEY'], expires_in=3600)
ACCEPTED_INPUT_FORMAT = ('Accepted input format is {\'name\''
                         ': \'Name 1\'}')

db.init_app(app)
app.app_context().push()

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


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


@app.route('/api/v1/', methods=['GET'])
def index():
    return return_response({'Message': ('Hello, World!,'
                                        ' This is the Home page')}, 200)


@app.route('/api/v1/auth/login', methods=['POST'])
def auth_login():
    username, password = get_request_data(request)

    dbs_exist()
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
    time_now = datetime.now()
    username, password = get_request_data(request)
    if not username or not password:
        return return_response(dict(
            Error='Your password or username is empty or wasn\'t found'), 500)

    dbs_exist()
    user_found = User.query.filter_by(username=username).first()
    if not user_found:
        pw_hash = generate_password_hash(password=password)
        save_user = User(username=username,
                         date_created=time_now,
                         date_modified=time_now,
                         password=pw_hash)
        save_user.save()
        return return_response(dict(Message='Registration Successful'), 201)
    return return_response(dict(Error='Username already exist'), 500)


@app.route('/api/v1/bucketlists', methods=['POST', 'GET'])
@multi_auth.login_required
def bucketlists():
    if request.method == 'POST':
        time_now = datetime.now()
        ret_value = request.json

        bucklist_name = '' if not ret_value else ret_value.get('name', '')
        if not bucklist_name:
            return return_response(dict(Error='Create Failed: %s'
                                              '' % ACCEPTED_INPUT_FORMAT), 500)

        all_current_bucketlist = BucketList.query.filter_by(
            created_by=g.user_id).all()
        bucketlist_names = [bucket.name for bucket in all_current_bucketlist]

        # check if the name was passed or exists
        if bucklist_name not in bucketlist_names:
            b_list = BucketList(name=bucklist_name,
                                date_created=time_now,
                                date_modified=time_now,
                                created_by=g.user_id)
            b_list.save()
        new_items = BucketList.query.filter_by(date_created=time_now).first()
        if new_items:
            new_items = new_items.get()
        else:
            new_items = dict(Message="Resource Created Successfully")
        return return_response(new_items, 201)

    if request.method == 'GET':
        count = 0
        time_now = datetime.now()
        return_bucketlists = {}

        limit = '20' if not request.args else request.args.get('limit', '20')
        limit = 20 if not limit.isdigit() else int(limit)

        if limit > 100:
            return return_response(
                dict(Error=('Get Failed: Only a maximum of 100 '
                            'items can be retrieved at ago')), 500)

        all_bucks = BucketList.query.filter_by(
            created_by=g.user_id).limit(limit).all()
        print ('q')
        q = '' if not request.args else request.args.get('q', '')
        if q:
            all_bucks = BucketList.query.filter(BucketList.name.contains(q))
            all_bucks = all_bucks.filter_by(created_by=g.user_id).all()

        if not all_bucks:
            return return_response(
                dict(Error=('Get Failed: No Bucketlists Found.')), 500)

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
    if request.method == 'GET':
        query = BucketList.query.filter_by(id=id, created_by=g.user_id).first()
        if not query:
            return return_response(dict(
                Error='Get Failed: Bucketlist Id %s was not found' % id), 500)
        query = query.get()

        query_items = Item.query.filter_by(bucketlist_id=id).all()
        query['item'] = Item().get_all(query_items)
        return return_response(query, 200)

    if request.method == 'PUT':
        time_now = datetime.now()
        query = BucketList.query.filter_by(id=id, created_by=g.user_id).first()
        if not query:
            return make_response(jsonify(dict(
                Error='Update Failed: Bucketlist Id %s '
                'was not found' % id)), 500)

        name = request.json.get('name', '')
        if not name:
            return return_response(dict(Error='Create Failed: %s'
                                              '' % ACCEPTED_INPUT_FORMAT), 500)
        query.name = name
        query.date_modified = time_now
        query.update()
        new_query = BucketList.query.filter_by(id=id).first()
        return return_response(new_query.get(), 201)

    if request.method == 'DELETE':
        query = BucketList.query.filter_by(id=id, created_by=g.user_id).first()
        if not query:
            return return_response(dict(
                Error='Delete Failed: Bucketlist Id %s '
                'was not found' % id), 500)
        query.delete()
        # Delete items associated with a given bucketlist
        query_items = Item.query.filter_by(bucketlist_id=id).all()
        for query_i in query_items:
            query_i.delete()
        return make_response(jsonify({}), 204)


@app.route('/api/v1/bucketlists/<int:id>/items', methods=['POST'])
@multi_auth.login_required
def bucketlists_id_items(id):
    ret_value = request.json

    n_item_name = '' if not ret_value else ret_value.get('name', '')
    if not n_item_name:
        return return_response(dict(Error='Create Failed: %s'
                                    '' % ACCEPTED_INPUT_FORMAT), 500)

    available_bucketlist = BucketList.query.filter_by(id=id).first()
    time_now = datetime.now()
    if not available_bucketlist:
        return return_response(dict(Error='Create Failed: Bucketlist Id'
                                    ' %s was not found' % id), 500)

    available_bucketlist.date_modified = time_now
    available_bucketlist.save()

    query_items = Item.query.all()
    item_names = [item.name for item in query_items]

    # Helps not to save a name already saved or not found
    if n_item_name not in item_names:
        item = Item(name=n_item_name)
        item.date_created = time_now
        item.date_modified = time_now
        item.bucketlist_id = available_bucketlist.id
        item.save()

    query_new = Item.query.filter_by(
        date_created=time_now, bucketlist_id=id).first()
    if query_new:
        query_new = query_new.get()
    else:
        query_new = dict(Message="Resource Created Successfully")

    return return_response(query_new, 201)


@app.route('/api/v1/bucketlists/<int:id>/items/<int:item_id>',
           methods=['PUT', 'DELETE'])
@multi_auth.login_required
def bucketlist_id_items_item_id(id, item_id):
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
                                        ' Id that is non existent '), 500)

        item_name = request.json.get('name', '')
        item_done = request.json.get('done', False)

        # Ensures that only boolean True is passed if not boolean False
        item_done = True if item_done else False

        if not item_name:
            return return_response(dict(Error='Update Failed: Item Name was'
                                        ' not found'), 500)

        query_items.name = item_name
        query_items.date_modified = time_now
        query_items.done = item_done
        query_items.update()

        query_bucketList.date_modified = time_now
        query_bucketList.update()

        query_updated_item = Item.query.filter_by(
            date_modified=time_now, id=query_items.id).first()
        if query_updated_item:
            query_updated_item = query_updated_item.get()
        else:
            query_updated_item = dict(Message="Resource Updated Successfully")
        return return_response(query_updated_item, 201)

    if request.method == 'DELETE':
        query_items = Item.query.filter_by(
            bucketlist_id=id, id=item_id).first()
        if not query_items:
            return return_response(
                dict(Error='Deleted Failed: You provided Item Id or'
                           ' BucketList Id that is non existent'), 500)
        query_items.delete()
        return return_response({}, 204)


@basic_auth.verify_password
def verify_password(username, password):
    dbs_exist()
    user_details = User.query.filter_by(username=username).first()
    g.user_id = 0
    if user_details and check_password_hash(
            user_details.password, password):
        g.user_id = user_details.id
        return True
    return False


@token_auth.verify_token
def verify_token(token):
    g.user_id = 0
    try:
        data = jwt.loads(token)['username']
    except:
        return False
    dbs_exist()
    users = User.query.filter_by(username=data.get('username', '')).first()
    if users:
        g.user_id = users.id
        return True
    return False


def generate_a_token(user):
    JWT(app.config['SECRET_KEY'], expires_in=3600)
    token = jwt.dumps({'username': user})
    return token.decode(encoding="utf-8")


def return_response(message, code):
    return jsonify(message), code


def dbs_exist():
    '''Method provides a help text if the tables don\'t exist'''
    help_text = {
        'Error': 'Databases not Found',
        'Recommendation': 'Delete Migrations folder and any db setup',
        'Command1': 'Run :\'python manage.py db init\'',
        'Command2': 'Run :\'python manage.py db migrate\'',
        'Command3': 'Run :\'python manage.py db upgrade\''
    }
    engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    user_table = engine.dialect.has_table(engine, 'user')
    bucketlist_table = engine.dialect.has_table(engine, 'bucketlist')
    items_table = engine.dialect.has_table(engine, 'items')

    if user_table and bucketlist_table and items_table:
        return True
    return_response(help_text, 500)


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
