# import json
from basetest import BaseTest
import json


class TestAppLiveServer(BaseTest):
    '''
    This Class is testing, if the correct status code is returned for
    a given route
    '''

    def test_homepage_return(self):
        '''Test retreiving the homePage return type'''
        response = self.http.get('/api/v1')
        self.assertEqual(dict(Message='Hello, World!, This is the Home page'),
                         response.json)
        self.assertEqual(200, response.status_code)

    def test_route_auth_register_code(self):
        '''Test registering of a new User'''
        register = {'username': 'Migwi', 'password': '1234'}
        response = self.http.post('/api/v1/auth/register',
                                  content_type='application/json',
                                  data=json.dumps(register)
                                  )
        self.assertEqual(201, response.status_code)
        self.assertEqual(dict(Message='Registration Successful'),
                         response.json)

    def test_route_Basic_auth_login_code(self):
        ''' Test Login using a password and username'''
        login_credentials = {"username": "Migwi", "password": "1234"}

        response = self.http.post('/api/v1/auth/login',
                                  content_type='application/json',
                                  data=json.dumps(login_credentials)
                                  )
        self.assertEqual(401, response.status_code)
        self.assertEqual({'Error': 'Login failed: Unauthorized access'},
                         response.json)

    def test_get_a_list_of_bucketlists(self):
        '''Test retrieving a list of bucketlists'''
        response = self.http.get('/api/v1/bucketlists',
                                 headers=self.auth_head)
        self.assertEqual(200, response.status_code)
        self.assertGreater(len(response.json), 1)

    def test_create_a_list_of_bucketlists(self):
        '''Test Creation of a new BucketList'''
        bucketlist_new = {"name": "Bucketlist2"}
        response = self.http.post('/api/v1/bucketlists',
                                  content_type='application/json',
                                  data=json.dumps(bucketlist_new),
                                  headers=self.auth_head
                                  )
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.json)

    def test_get_bucketlist_with_id(self):
        '''Test retrieving a bucketlist with a given Id'''
        response = self.http.get('/api/v1/bucketlists/1',
                                 headers=self.auth_head)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json)

    def test_edit_bucketlist_with_id(self):
        '''Test editting a bucketlist with a given Id'''
        bucketlist = {"name": "Visit Canadian Rockies"}
        response = self.http.put('/api/v1/bucketlists/1',
                                 content_type='application/json',
                                 data=json.dumps(bucketlist),
                                 headers=self.auth_head
                                 )
        self.assertEqual(201, response.status_code)
        self.assertEqual('Visit Canadian Rockies',
                         response.json.get('name', ''))

    def test_delete_bucketlist_with_id(self):
        '''Test Deleting a Bucketlist with a given Id'''
        response = self.http.delete('/api/v1/bucketlists/1',
                                    headers=self.auth_head)
        self.assertEqual(204, response.status_code)

    def test_create_task_in_bucketlist_with_id(self):
        '''Test creating a task in BucketList with the given Id'''
        task = {"name": "Visit Andela New York Office"}
        response = self.http.post('/api/v1/bucketlists/1/items',
                                  content_type='application/json',
                                  data=json.dumps(task),
                                  headers=self.auth_head
                                  )
        self.assertEqual(201, response.status_code)
        self.assertEqual(task['name'], response.json.get('name', ''))

    def test_modify_task_in_bucketlist_with_id(self):
        '''Test Modifying a task in a Bucketlist with a  given Id'''
        task_new = {"name": "Visit Andela Nigeria Office",
                    "done": True
                    }
        response = self.http.put('/api/v1/bucketlists/1/items/2',
                                 content_type='application/json',
                                 data=json.dumps(task_new),
                                 headers=self.auth_head)
        self.assertEqual(201, response.status_code)
        self.assertTrue(response.json.get('done', ''))

    def test_delete_task_in_bucketlist_with_id(self):
        '''Test Deleting a task in a BucketList with the given Id'''
        response = self.http.delete('/api/v1/bucketlists/1/items/3',
                                    headers=self.auth_head)
        self.assertEqual(204, response.status_code)
