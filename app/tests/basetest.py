import tempfile
from manage import app as app_test, db
from app.models import Item, User, BucketList
from datetime import datetime
from flask_testing import TestCase
from itsdangerous import TimedJSONWebSignatureSerializer as JWT


class BaseTest(TestCase):

    def create_app(self):
        app_test.config['DATABASE'] = tempfile.mkstemp()
        app_test.config['TESTING'] = True
        app_test.config['SECRET_KEY'] = 'the tests refactoring'
        app_test.config['TRAP_HTTP_EXCEPTIONS'] = True

        app_test.config['DEBUG'] = True
        self.jwt = JWT(app_test.config['SECRET_KEY'], expires_in=360)

        # db.init_app(app_test)
        self.app_t = app_test
        db.create_all(app=self.app_t)
        return app_test

    def setUp(self):
        self.json_head = {'Content-Type': 'application/json'}

        self.http = self.create_app().test_client()

        # To hold contentType and Token headers
        self.auth_json_head = self.json_head.copy()

        # Create and add a user to the db
        user = User(username='andela-dmigwi', password='migwi123')
        user.save()

        # Add a BucketList to the db
        bucketlist = BucketList(name='December Vacation',
                                date_created=datetime.now(),
                                date_modified=datetime.now()
                                )
        bucketlist.save()

        # Add Items to the db
        # Task 1
        tasks1 = Item(name='Visit Nigeria',
                      bucketlist_id=1,
                      date_created=datetime.now(),
                      date_modified=datetime.now(),
                      done=False)
        tasks1.save()

        # Task 2
        tasks2 = Item(name='Visit New York',
                      bucketlist_id=1,
                      date_created=datetime.now(),
                      date_modified=datetime.now(),
                      done=False)
        tasks2.save()

        # Task 3
        tasks3 = Item(name='Visit Las Vegas',
                      bucketlist_id=1,
                      date_created=datetime.now(),
                      date_modified=datetime.now(),
                      done=False)
        tasks3.save()

        user = {'username': 'andela-dmigwi',
                            'password': 'migwi123'}
        token = self.jwt.dumps({'username': user})
        # token = token.decode(encoding="utf-8")
        token = '7823ed23uhduih3d32'

        # retrieve a token and assign to the Auth_head
        if token:
            self.auth_head = {'Authorization': 'Bearer %s' % token}
            # self.auth_json_head.update(self.auth_head)
        else:
            raise Exception('No Token Was Found')

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app_t)
