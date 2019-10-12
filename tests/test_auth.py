from flask import url_for

from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Create Snippets', data)
        self.assetNotIn('Sign in', data)

    def test_fail_login(self):
        response = self.login(email="wrong@test.com", password='wrong-password')
        data = response.get_data(as_text=True)
        self.assertIn('Either the email or password was incorrect.', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertNotIn('Create Snippets', data)
        self.assertIn('Sign in', data)
