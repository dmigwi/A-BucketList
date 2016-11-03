# import json
from basetest import BaseTest


class TestAppLiveServer(BaseTest):
    '''
    This Class is testing, if the correct status code is returned for
    a given route
    '''

    def test_homepage_return(self):
        '''Test retreiving the homePage return type'''
        response = self.http.get('/api/v1/')
        self.assertEqual(dict(data='Hello, World!, This is the Home page'),
                         response.json)
        self.assertIn('200', response.status)

    def test_route_auth_register_code(self):
        '''Test registering of a new User'''
        register = {'username': 'Migwi', 'password': '1234'}
        response = self.http.post('/api/v1/auth/register',
                                  data=register,
                                  headers=self.json_head)
        self.assertIn('201', response.status)
        self.assertEqual(register, response.json)

    def test_route_Basic_auth_login_code(self):
        ''' Test Login using a password and username'''
        login_credentials = {'username': 'Migwi', 'password': '1234'}
        response = self.http.post('/api/v1/auth/login',
                                  data=login_credentials,
                                  headers=self.json_head,
                                  follow_redirects=True)
        self.assertIn('201', response.status)

    def test_get_a_list_of_bucketlists(self):
        '''Test retrieving a list of bucketlists'''
        response = self.http.get('/api/v1/bucketlists',
                                 headers=self.auth_head)
        self.assertIn('200', response.status)
        self.assertGreater(len(response.json), 0)

    def test_create_a_list_of_bucketlists(self):
        '''Test Creation of a new BucketList'''
        bucketlist_new = {
            'name': 'Bucketlist2'
        }
        response = self.http.post('/api/v1/bucketlists',
                                  data=bucketlist_new,
                                  headers=self.auth_json_head)
        self.assertIn('201', response.status)
        self.assertEqual('Bucketlist2', response.json.get('name', ''))

    def test_get_bucketlist_with_id(self):
        '''Test retrieving a bucketlist with a given Id'''
        response = self.http.get('/api/v1/bucketlists/2',
                                 headers=self.auth_head)
        self.assertIn('200', response.status)
        self.assertNotNone(response.json)

    def test_edit_bucketlist_with_id(self):
        '''Test editting a bucketlist with a given Id'''
        bucketlist = {
            'name': 'Visit Canadian Rockies'
        }
        response = self.http.put('/api/v1/bucketlists/2',
                                 data=bucketlist,
                                 headers=self.auth_json_head)
        self.assertIn('201', response.status)
        self.assertEqual('Visit Canadian Rockies',
                         response.json.get('name', ''))

    def test_delete_bucketlist_with_id(self):
        '''Test Deleting a Bucketlist with a given Id'''
        response = self.http.delete('/api/v1/bucketlists/2',
                                    headers=self.auth_head)
        self.assertIn('204', response.status)
        self.assertEqual(dict(data='Delete Successful'),
                         response.json)

    def test_create_task_in_bucketlist_with_id(self):
        '''Test creating a task in BucketList with the given Id'''
        task = {
            'name': 'Visit Andela New York Office',
            'done': False
        }
        response = self.http.post('/api/v1/bucketlists/1/items',
                                  data=task,
                                  headers=self.auth_json_head)
        self.assertIn('201', response.status)
        self.assertEqual('Visit Andela New York Office',
                         response.json.get('name', ''))

    def test_modify_task_in_bucketlist_with_id(self):
        '''Test Modifying a task in a Bucketlist with a  given Id'''
        task_new = {
            'name': 'Visit Andela Nigeria Office',
            'done': True
        }
        response = self.http.put('/api/v1/bucketlists/1/items/1',
                                 data=task_new,
                                 headers=self.auth_json_head)
        self.assertIn('201', response.status)
        self.assertTrue(response.json.get('done', ''))

    def test_delete_task_in_bucketlist_with_id(self):
        '''Test Deleting a task in a BucketList with the given Id'''
        response = self.http.delete('/api/v1/bucketlists/1/items/1',
                                    headers=self.auth_head)
        self.assertIn('204', response.status)
        self.assertEqual(dict(data='Delete Successful'),
                         response.json)
