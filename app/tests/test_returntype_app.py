from basetest import BaseTest
import json


class TestAppReturnType(BaseTest):
    '''
    This Class test if the correct information is returned by a
    a given route
    '''

    def test_login_with_wrong_credentails(self):
        '''Test Error returned when wrong login credentials are used'''
        login_credentials = {"username": "post", "password": "post"}
        response = self.http.post('/api/v1/auth/login',
                                  content_type='application/json',
                                  data=json.dumps(login_credentials),
                                  headers={'Accept': 'application/json'}
                                  )
        self.assertEqual(
            dict(Error='Login failed: Unauthorized access'),
            response.json)

    def test_login_with_correct_credentials(self):
        '''Test if a token is returned after a successful login'''
        login_credential = {'username': 'andela-dmigwi',
                            'password': 'migwi123'}
        response = self.http.post('/api/v1/auth/login',
                                  content_type='application/json',
                                  data=json.dumps(login_credential),
                                  headers={'Accept': 'application/json'}
                                  )
        self.assertIn('Bearer', response.json.get('Authorization', ''))

    def test_get_specified_number_of_bucketlists(self):
        '''Test if the specified No. of BucketLists is returned'''
        response = self.http.get('/api/v1/bucketlists?limit=%s' % 20,
                                 headers=self.auth_head
                                 )
        self.assertLess(len(response.json), 21)

    def test_get_too_much_number_of_bucketlists(self):
        '''TEst error returned when bucketlists more than 100 is requested'''
        response = self.http.get('/api/v1/bucketlists?limit=%s' % 2000,
                                 headers=self.auth_head
                                 )
        self.assertEquals(
            dict(Error=('Get Failed: Only a maximum of 100'
                        ' items can be retrieved at ago')),
            response.json)

    def test_create_bucketlist_without_name(self):
        '''Test error returned when bucketlist name is not provided'''
        bucketlistss = {'name': ''}
        response = self.http.post('/api/v1/bucketlists',
                                  content_type='application/json',
                                  data=json.dumps(bucketlistss),
                                  headers=self.auth_head
                                  )
        self.assertEquals(
            dict(Error='Create Failed: Accepted input format '
                 'is {\'name\': \'Name 1\'}'), response.json)

    def test_get_bucketlist_not_available(self):
        '''
        Test error returned when bucketlist bieng retrieved doesn't exist
        '''
        response = self.http.get('/api/v1/bucketlists/1000',
                                 headers=self.auth_head
                                 )
        self.assertEquals(
            dict(Error='Get Failed: Bucketlist Id 1000 was not found'),
            response.json)

    def test_update_bucketlist_not_available(self):
        '''
        Test error returned when update is being
        made on a none existent bucketlist
        '''
        bucketlists = {'name': 'Learn how to Use Vim'}
        response = self.http.put('/api/v1/bucketlists/1000',
                                 headers=self.auth_head,
                                 data=json.dumps(bucketlists)
                                 )
        self.assertEqual(
            dict(Error='Update Failed: Bucketlist Id 1000 was not found'),
            response.json)

    def test_delete_bucketlist_not_available(self):
        '''Test error returned when a none existent bucketlist
         is being deleted'''
        response = self.http.delete('/api/v1/bucketlists/1000',
                                    headers=self.auth_head
                                    )
        self.assertEqual(
            dict(Error='Delete Failed: Bucketlist Id 1000 was not found'),
            response.json)

    def test_create_items_in_a_non_existent_bucketlist(self):
        '''Test error returned when a task  is being created
        in a none existent bucketlist'''
        items = {'name': 'This does not exist'}
        self.auth_head.update({'Accept': 'application/json'})
        response = self.http.post('/api/v1/bucketlists/2000/items',
                                  headers=self.auth_head,
                                  content_type='application/json',
                                  data=json.dumps(items)
                                  )
        self.assertEqual(
            dict(Error='Create Failed: Bucketlist Id 2000 was not found'),
            response.json)

    def test_update_item_in_bucketlist_that_doesnt_exist(self):
        '''Test error returned when a task update is being
         made in a none existent bucketlist'''
        items = {'name': 'This doesnt exist',
                 'done': True}
        response = self.http.put('/api/v1/bucketlists/2000/items/1',
                                 headers=self.auth_head,
                                 content_type='application/json',
                                 data=json.dumps(items)
                                 )
        self.assertEqual(
            dict(Error=('Update Failed: You provided Item Id or BucketList'
                        ' Id that is non existent ')), response.json)

    def test_delete_item_in_bucketlist_that_doesnt_exist(self):
        '''Test error returned when a task is being deleted
        in none existent bucketlist'''
        response = self.http.delete('/api/v1/bucketlists/2000/items/1',
                                    headers=self.auth_head
                                    )
        self.assertEqual(
            dict(Error='Deleted Failed: You provided Item Id or BucketList'
                 ' Id that is non existent'), response.json)

    def test_update_item_not_in_bucketlist(self):
        '''Test error returned when a none existent task is bieng updated'''
        items = {'name': 'This doesnt exist',
                 'done': True}
        response = self.http.put('/api/v1/bucketlists/1/items/1121',
                                 content_type='application/json',
                                 headers=self.auth_head,
                                 data=json.dumps(items)
                                 )
        self.assertEqual(
            dict(Error=('Update Failed: You provided Item Id or BucketList'
                        ' Id that is non existent ')), response.json)

    def test_delete_item_not_in_bucketlist(self):
        '''Test error returned when a none existent task is being deleted'''
        response = self.http.delete('/api/v1/bucketlists/1/items/1234',
                                    headers=self.auth_head
                                    )
        self.assertEqual(
            dict(Error=('Deleted Failed: You provided Item Id or BucketList Id'
                        ' that is non existent')), response.json)
