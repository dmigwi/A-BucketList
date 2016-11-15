
"""
This File hold help messages that should guide the user
if need be
"""

help_text = {
    '**Error': 'Databases not Found!!',
    '**Recommendation': 'Delete Migrations folder first:',
    'Command1': 'Run :\'python manage.py db init\'',
    'Command2': 'Run :\'python manage.py db migrate\'',
    'Command3': 'Run :\'python manage.py db upgrade\''
}

help_message = {
    'Copyright': ('This an python Bucketlist api built by Migwi '
                  'Ndung\'u :**https://github.com/andela-dmigwi/'
                  'A-BucketList**'),
    'Credits_To': ('Alex Mwaleh, Hassan Oyeboade,'
                   ' Percila Njira and Others'),
    'route_1': '/api/v1 (GET) Shows HomePage',
    'route_2': '/api/v1/auth/register (POST) register a new user',
    'route_3': ('/api/v1/auth/login (POST) obtain token and'
                ' put it in Authorization header'),
    'route_4': ('/api/v1/bucketlists (GET) get all bucketlist;'
                ' (POST) Create new bucketlists'),
    'route_5': ('/api/v1/bucketlists/<int:id> (PUT) modify; '
                '(GET) Retrieve; (DELETE) delete one bucketlist'),
    'route_6': ('/api/v1/bucketlists/<int:id>/items (POST)'
                ' create new bucketlist item '),
    'route_7': ('/api/v1/bucketlists/<int:id>/items<int:id>'
                ' (PUT) modify (DELETE) delete an item')
}
