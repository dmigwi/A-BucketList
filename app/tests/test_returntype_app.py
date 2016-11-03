from basetest import BaseTest


class TestAppReturnType(BaseTest):
    '''
    This Class test if the correct information is returned by a
    a given route
    '''

    def test_homepage_return(self):
        response = self.http.get('/')
        self.assertEqual(dict(data='Hello, World!, This is the Home page'),
                         response.json)

    def test_registration_of_new_user(self):
        reg_details = {'username': 'aaa', 'password': 'aaaa'}
        response = self.http.post(
            '/auth/register',
            data=reg_details,
            headers=self.json_head
        )
        self.assertEqual(reg_details,
                         response.json)

    def test_login_with_wrong_credentails(self):
        login_credentails = {'username': 'post', 'password': 'post'}
        response = self.http.post(
            '/auth/login',
            data=login_credentails,
            headers=self.json_head,
            follow_redirects=True
        )
        self.assertEqual(
            dict(data='You provided a Wrong Password or Username'),
            response.json)

    def test_login_with_correct_credentials(self):
        login_credential = {'username': 'andela-dmigwi',
                            'password': 'migwi123'}
        response = self.http.post(
            '/auth/login',
            data=login_credential,
            headers=self.json_head,
            follow_redirects=True
        )
        self.assertIn('Bearer', response.json.get('Authorization', ''))

    def test_get_specified_number_of_bucketlists(self):
        response = self.http.get(
            '/bucketlists', data={'limit': 20},
            headers=self.auth_json_head)
        self.assertEquals(len(response.json), 20)

    def test_get_too_much_number_of_bucketlists(self):
        response = self.http.get(
            '/bucketlists', data={'limit': 2000},
            headers=self.auth_json_head)
        self.assertEquals(
            dict(error='Only a maximum of 100 items can be retrieved at ago'),
            response.json)

    def test_create_bucketlist_without_name(self):
        bucketlist = {'name': ''}
        response = self.http.post(
            '/bucketlists',
            data=bucketlist,
            headers=self.auth_json_head)
        self.assertEquals(
            dict(error='Bucketlist name is either too short or not found'),
            response.json)

    def test_get_bucketlist_not_available(self):
        response = self.http.get(
            '/bucketlists/1000',
            headers=self.auth_head
        )
        self.assertEquals(
            dict(error='Create Failed: Bucketlist Id 1000 was not found'),
            response.json)

    def test_update_bucketlist_not_available(self):
        bucketlists = {'name': 'Learn how to Use Vim'}
        response = self.http.put(
            '/bucketlists/1000',
            data=bucketlists,
            headers=self.auth_json_head
        )
        self.assertEqual(
            dict(error='Update Failed: Bucketlist Id 1000 was not found'),
            response.json)

    def test_delete_bucketlist_not_available(self):
        response = self.http.delete(
            '/bucketlists/1000',
            headers=self.auth_head
        )
        self.assertEqual(
            dict(error='Delete Failed: Bucketlist Id 1000 was not found'),
            response.json)

    def test_create_items_in_a_non_existent_bucketlist(self):
        items = {'name': 'This doesn\'t exist',
                 'done': False}
        response = self.http.post(
            '/bucketlists/2000/items',
            data=items,
            headers=self.auth_json_head
        )
        self.assertEqual(
            dict(error='Create Failed: Bucketlist Id 2000 was not found'),
            response.json)

    def test_update_item_in_bucketlist_that_doesnt_exist(self):
        items = {'name': 'This doesnt exist',
                 'done': True}
        response = self.http.put(
            '/bucketlists/2000/items/1',
            data=items,
            headers=self.auth_json_head
        )
        self.assertEqual(
            dict(error='Update Failed: Bucketlist Id 2000 was not found'),
            response.json)

    def test_delete_item_in_bucketlist_that_doesnt_exist(self):
        response = self.http.delete(
            '/bucketlists/2000/items/1',
            headers=self.auth_head
        )
        self.assertEqual(
            dict(error='Delete Failed: Bucketlist Id 2000 was not found'),
            response.json)

    def test_update_item_not_in_bucketlist(self):
        items = {'name': 'This doesnt exist',
                 'done': True}
        response = self.http.put(
            '/bucketlists/1/items/1121',
            data=items,
            headers=self.auth_json_head
        )
        self.assertEqual(
            dict(error='Update Failed: Item Id 1121 was not found'),
            response.json)

    def test_delete_item_not_in_bucketlist(self):
        response = self.http.delete(
            '/bucketlists/1/items/1234',
            headers=self.auth_head
        )
        self.assertEqual(
            dict(error='Delete Failed: Item Id 1234 was not found'),
            response.json)
