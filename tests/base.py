import os

os.environ['GITHUB_CLIENT_ID'] = 'test'
os.environ['GITHUB_CLIENT_SECRET'] = 'test'
os.environ['GOOGLE_CLIENT_ID'] = 'test'
os.environ['GOOGLE_CLIENT_SECRET'] = 'test'
os.environ['TWITTER_CLIENT_ID'] = 'test'
os.environ['TWITTER_CLIENT_SECRET'] = 'test'

import unittest

from flask import url_for

from app import create_app
from app.extensions import db
from app.models import User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        user = User(nickname='Tester', email="common_user@test.com")
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, email=None, password=None):
        if email is None and password is None:
            email = 'common_user@test.com'
            password = '123456'

        return self.client.post(url_for('auth.login'), data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)
