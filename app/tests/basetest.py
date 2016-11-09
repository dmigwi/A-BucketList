from manage import app as app_test, db
from app.models import Item, User, BucketList
from datetime import datetime
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
import logging as log


class BaseTest(TestCase):

    def create_app(self):
        app_test.config.from_object('config.TestingConfig')
        self.jwt = JWT(app_test.config['SECRET_KEY'], expires_in=3600)

        self.app_t = app_test
        return app_test

    def setUp(self):
        db.create_all(app=self.app_t)

        self.today = datetime.now().strftime('%Y-%m-%d')
        self.http = self.create_app().test_client()

        # Create and add a user to the db
        user = User(username='andela-dmigwi',
                    password=generate_password_hash('migwi123'))
        user.save()

        # Add a BucketList to the db
        bucketlist = BucketList(name='December Vacation',
                                date_created=datetime.now(),
                                date_modified=datetime.now(),
                                created_by=1
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
        token = token.decode(encoding="utf-8")

        # retrieve a token and assign to the Auth_head
        if token:
            self.auth_head = {'Authorization': 'Bearer %s' % token}
        else:
            log.error('No Token Was Found')

        # Add Other Users
        user = User(username='andela-njirap',
                    password=generate_password_hash('njirap123'))
        user.save()

        user = User(username='andela-kimani',
                    password=generate_password_hash('kimani123'))
        user.save()

        # Add a BucketList to the db
        bucketlist = BucketList(name='Visit Kenya',
                                date_created=datetime.now(),
                                date_modified=datetime.now(),
                                created_by=1
                                )
        bucketlist.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app_t)
