from flask import url_for

from .base import BaseTestCase
from app.extensions import db
from app.models import User


class AdminTestCase(BaseTestCase):

    def setUp(self):
        super(AdminTestCase, self).setUp()
        admin = User(email='12@test.com', nickname='Admin Tester')
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()

    def test_admin_permission(self):
        # ? test anonymous user to delete user should fail
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 403)
        # ? test common user to delete user should fail
        self.login()
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 403)

    def test_block_admin(self):
        # ? test admin user to delete self/ admin user should fail
        self.login(email="12@test.com", password='123456')
        response = self.client.delete(url_for('admin.block_user', user_id=2))
        self.assertEqual(response.status_code, 400)

    def test_block_user(self):
        # ? test admin user to delete common user should fail
        self.login(email='12@test.com', password='123456')
        response = self.client.delete(url_for('admin.block_user', user_id=1))
        self.assertEqual(response.status_code, 204)
        # common user with id of 1 is gone
        self.assertIsNone(User.query.get(1))
