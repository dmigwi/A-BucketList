# import os
from app.app import app
from app.models import db
from flask_testing import TestCase
import tempfile


class TestApp(TestCase):

    def create_app(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()
        db.init_app(app)
        db.create_all(app=app)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=app)

    def test_homepage_return(self):
        response = self.client.get('/')
        self.assertEqual(response.json,
                         dict(data='Hello, World!, This is the Home page'))
