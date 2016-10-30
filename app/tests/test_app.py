import simplejson as json
import tempfile
import urllib3
from app.app import app
from app.models import db
from flask_testing import TestCase, LiveServerTestCase


class TestAppReturnType(TestCase):
    '''
    This Class test is the correct information is returned by a
    a given route
    '''

    def create_app(self):
        app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        db.init_app(app)
        db.create_all(app=app)

        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=app)

    def test_homepage_return(self):
        response = self.client.get('/')
        self.assertEqual(dict(data='Hello, World!, This is the Home page'),
                         json.loads(response.data))


class TestAppLiveServer(LiveServerTestCase):
    '''
    This Class does a Live server testing,
    It tests if the correct status code is returned for
    a given route
    '''

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943  # Default port is 5000
        app.config['LIVESERVER_TIMEOUT'] = 10  # Default timeout is 5 seconds
        return app

    def setUp(self):
        self.host = self.get_server_url()
        self.http = urllib3.PoolManager()

    def test_server_is_up_and_running(self):
        response = self.http.request('GET', self.host + '/')
        self.assertEqual(response.status, 200)

    def test_route_auth_register_code(self):
        register = {'username': 'Migwi', 'password': '1234'}
        response = self.http.request('POST', self.host + '/auth/register',
                                     body=json.dumps(register),
                                     headers={'Content-Type':
                                              'application/json'})
        self.assertEqual(response.status, 201)

    def test_route_Basic_auth_login_code(self):
        # Login using a password and username or email
        login_credentials = {'username': 'Migwi', 'password': '1234'}
        response = self.http.request('POST', self.host + '/auth/login',
                                     body=json.dumps(login_credentials),
                                     headers={'Content-Type':
                                              'application/json'})
        self.assertEqual(response.status, 201)

    def test_route_token_login_auth(self):
        # Login using a token
        login_token = {'Authorization': 'Bearer uwyriuwyruiw'}
        response = self.http.request('POST', self.host + '/auth/login',
                                     body=json.dumps(login_token),
                                     headers={'Content-Type':
                                              'application/json'})
        self.assertEqual(response.status, 201)

    def test_get_a_list_of_bucketlists(self):
        response = self.http.request('GET', self.host + '/bucketlists')
        self.assertEqual(response.status, 200)

    def test_create_a_list_of_bucketlists(self):
        bucketlist_new = {
            'name': 'Bucketlist1',
            'item': [],
            'date_created': '2015-08-12 11:57:23',
            'date_modified': '2015-08-12 11:57:23'
        }
        response = self.http.request('POST', self.host + '/bucketlists',
                                     body=json.dumps(bucketlist_new),
                                     headers={'Content-Type':
                                              'application/json'})
        self.assertEqual(response.status, 201)

    def test_get_bucketlist_with_id(self):
        response = self.http.request('GET', self.host + '/bucketlists/2')
        self.assertEqual(response.status, 200)

    def test_edit_bucketlist_with_id(self):
        bucketlist = {
            'name': 'Bucketlist2',
            'item': [],
            'date_created': '2016-08-12 11:57:23',
            'date_modified': '2016-08-12 11:57:23'
        }
        response = self.http.request('PUT', self.host + '/bucketlists/2',
                                     body=json.dumps(bucketlist),
                                     headers={'Content-Type':
                                              'application/json'})
        self.assertIn(response.status, [200, 204])

    def test_delete_bucketlist_with_id(self):
        response = self.http.request('DELETE', self.host + '/bucketlists/2')
        self.assertIn(response.status, [200, 202, 204])

    def test_create_task_in_bucketlist_with_id(self):
        task = {
            'name': 'Visit Andela New York Office',
            'bucketlist_id': 2,
            'date_created': '2016-08-12 13:57:23',
            'date_modified': '2016-08-12 13:57:23',
            'done': False
        }
        response = self.http.request('POST',
                                     self.host + '/bucketlists/1/items',
                                     body=json.dumps(task),
                                     headers={'Content-Type':
                                              'application/json'})
        self.assertEqual(response.status, 201)

    def test_modify_task_in_bucketlist_with_id(self):
        task_new = {
            'name': 'Visit Andela New York Office',
            'bucketlist_id': 2,
            'date_created': '2016-08-12 13:57:23',
            'date_modified': '2016-31-12 13:57:23',
            'done': True
        }
        response = self.http.request('PUT',
                                     self.host + '/bucketlists/1/items/1',
                                     body=json.dumps(task_new),
                                     headers={'Content-Type':
                                              'application/json'})
        self.assertIn(response.status, [200, 204])

    def test_delete_task_in_bucketlist_with_id(self):
        response = self.http.request('DELETE',
                                     self.host + '/bucketlists/1/items/1')
        self.assertIn(response.status, [200, 202, 204])
