from basetest import BaseTest, User, Item, BucketList


class TestModels(BaseTest):

    def test_save(self):
        '''Test if a new user is saved'''
        users = User.query.filter_by(username='arnold').first()
        self.assertIsNone(users)

        new_user = User(username='arnold', password='1234')
        new_user.save()

        new_users = User.query.filter_by(username='arnold').first()
        self.assertEqual('arnold', new_users.username)

    def test_update(self):
        '''Test if the Update()'''
        users = User.query.filter_by(username='andela-dmigwi').first()
        self.assertEqual('migwi123', users.password)

        users.password = 'this_is_a_test_password'
        users.update()

        updated_user = User.query.filter_by(username='andela-dmigwi').first()
        self.assertEqual(users, updated_user)

    def test_delete(self):
        '''Test delete()'''
        user_to_delete = User.query.filter_by(username='andela-dmigwi').first()
        self.assertEqual('andela-dmigwi', user_to_delete.username)

        user_to_delete.delete()
        deleted_user = User.query.filter_by(username='andela-dmigwi').first()
        self.assertIsNone(deleted_user)

    def test_get_user(self):
        '''Test User.get()'''
        get_user = User.query.filter_by(username='andela-njirap').first()
        user_details = get_user.get()

        int_id = user_details.get('id', -1)
        self.assertGreater(int_id, 0)
        self.assertEqual('andela-njirap', user_details.get('username', ''))
        self.assertEqual('njirap123', user_details.get('password', ''))

    def test_get_bucketlist(self):
        '''Test BucketList.get()'''
        get_bucketlist = BucketList.query.filter_by(
            name='December Vacation').first()
        bucketlist_details = get_bucketlist.get()

        int_id = int(bucketlist_details.get('id', -1))
        self.assertGreater(int_id, 0)
        self.assertEqual('December Vacation',
                         bucketlist_details.get('name', ''))
        self.assertIsNotNone(bucketlist_details.get('date_created', ''))
        self.assertIsNotNone(bucketlist_details.get('date_modified', ''))

    def test_get_bucketlist_item(self):
        '''Test Item.get()'''
        get_bucketlist_item = Item.query.filter_by(
            name='Visit Nigeria').first()
        item_details = get_bucketlist_item.get()

        int_id = int(item_details.get('id', -1))
        self.assertGreater(int_id, 0)
        self.assertEqual('Visit Nigeria',
                         item_details.get('name', ''))
        self.assertIsNotNone(item_details.get('date_created', ''))
        self.assertIsNotNone(item_details.get('date_modified', ''))
        self.assertFalse(item_details.get('done', True))
