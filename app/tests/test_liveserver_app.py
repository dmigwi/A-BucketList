import json
from basetest import BaseTest


class TestAppLiveServer(BaseTest):
    '''
    This Class does a Live server testing,
    It tests if the correct status code is returned for
    a given route
    '''

    def test_server_is_up_and_running(self):
        response = self.http.get('/')
        self.assertEqual(response.status, 200)

    def test_route_auth_register_code(self):
        '''Test registering of a new User'''
        register = {'username': 'Migwi', 'password': '1234'}
        response = self.http.post('/auth/register',
                                  data=json.dumps(register),
                                  headers=self.json_head)
        self.assertEqual(response.status, 201)
        self.assertEqual(register, response.json)

    def test_route_Basic_auth_login_code(self):
        ''' Test Login using a password and username'''
        login_credentials = {'username': 'Migwi', 'password': '1234'}
        response = self.http.post('/auth/login',
                                  data=json.dumps(login_credentials),
                                  headers=self.json_head,
                                  follow_redirects=True)
        self.assertEqual(response.status, 200)
        self.assertIn('Bearer', response.json.get('Authorization', ''))

    def test_get_a_list_of_bucketlists(self):
        '''Test retrieving a list of bucketlists'''
        response = self.http.get('/bucketlists',
                                 headers=self.auth_head)
        self.assertEqual(response.status, 200)
        self.assertGreater(len(response.json), 0)

    def test_create_a_list_of_bucketlists(self):
        '''Test Creation of a now BucketList'''
        bucketlist_new = {
            'name': 'Bucketlist2'
        }
        response = self.http.post('/bucketlists',
                                  data=json.dumps(bucketlist_new),
                                  headers=self.auth_json_head)
        self.assertEqual(response.status, 201)
        self.assertEqual('Bucketlist2', response.json['name'])

    def test_get_bucketlist_with_id(self):
        '''Test retrieve a bucketlist with a given Id'''
        response = self.http.get('/bucketlists/2',
                                 headers=self.auth_head)
        self.assertEqual(response.status, 200)
        self.assertNotNone(response.json)

    def test_edit_bucketlist_with_id(self):
        '''Test editting a bucketlist with a given Id'''
        bucketlist = {
            'name': 'Visit Canadian Rockies'
        }
        response = self.http.put('/bucketlists/2',
                                 data=json.dumps(bucketlist),
                                 headers=self.auth_json_head)
        self.assertIn(response.status, [200, 204])
        self.assertEqual('Visit Canadian Rockies',
                         response.json.get('name', ''))

    def test_delete_bucketlist_with_id(self):
        '''Test Delete a Bucketlist with a given Id'''
        response = self.http.delete('/bucketlists/2',
                                    headers=self.auth_head)
        self.assertIn(response.status, [200, 202, 204])
        self.assertEqual(dict(data='Delete Successful'),
                         response.json)

    def test_create_task_in_bucketlist_with_id(self):
        '''Test create a task in BucketList with the given Id'''
        task = {
            'name': 'Visit Andela New York Office',
            'done': False
        }
        response = self.http.post('/bucketlists/1/items',
                                  data=json.dumps(task),
                                  headers=self.auth_json_head)
        self.assertEqual(response.status, 201)
        self.assertEqual('Visit Andela New York Office',
                         response.json.get('name', ''))

    def test_modify_task_in_bucketlist_with_id(self):
        '''Test Modify a task in a Bucketlist with a  given Id'''
        task_new = {
            'name': 'Visit Andela Nigeria Office',
            'done': True
        }
        response = self.http.put('/bucketlists/1/items/1',
                                 data=json.dumps(task_new),
                                 headers=self.auth_json_head)
        self.assertIn(response.status, [200, 204])
        self.assertTrue(response.json.get('done', ''))

    def test_delete_task_in_bucketlist_with_id(self):
        '''Test Delete a task in a BucketList with the given Id'''
        response = self.http.delete('/bucketlists/1/items/1',
                                    headers=self.auth_head)
        self.assertIn(response.status, [200, 202, 204])
        self.assertEqual(dict(data='Delete Successful'),
                         json.loads(response.data))
