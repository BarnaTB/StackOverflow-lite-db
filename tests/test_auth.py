import unittest
import json
from api.models import User
from api import app
from database.db import DbConnection


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.db = DbConnection()
        self.tester = app.test_client(self)

    def test_register_successfully(self):
        """Test successful user registration"""
        user = dict(
            username='username',
            email='username@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 201)

    def test_registration_empty_username(self):
        user = dict(
            username="",
            email="barna@gmail.com",
            password="123456"
        )

        response = self.tester.post(
                'api/v1/signup',
                content_type='application/json',
                data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(
            reply["message"], "Sorry, you did not enter your username!"
            )

    def test_registration_spaces_entry(self):
        user = dict(
            username=" ",
            email="barna@gmail.com",
            password="123456"
        )

        response = self.tester.post(
                'api/v1/signup',
                content_type='application/json',
                data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(
            reply["message"], "Sorry, you did not enter your username!"
            )

    def test_registration_email_empty(self):
        user = dict(
            username="Barna",
            email="",
            password="123456"
        )

        response = self.tester.post(
                'api/v1/signup',
                content_type='application/json',
                data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(
            reply["message"], "Sorry, you did not enter your email!"
            )

    def test_registration_email_space_entry(self):
        user = dict(
            username="Barna",
            email=" ",
            password="123456"
        )

        response = self.tester.post(
                'api/v1/signup',
                content_type='application/json',
                data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"], "Sorry, you did not enter your email!")

    def test_registration_email_vague_data(self):
        user = dict(
            username="Barna",
            email="barna@..Com",
            password="123456"
        )

        response = self.tester.post(
                'api/v1/signup',
                content_type='application/json',
                data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"], "Invalid email address!")

    def test_registration_password_empty(self):
        user = dict(
            username="Barna",
            email="barna@gmail.Com",
            password=""
        )

        response = self.tester.post(
                'api/v1/signup',
                content_type='application/json',
                data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"], "Sorry, you did not enter your password!")

    def registration_password_spaces_entry(self):
        user = dict(
            username="Barna",
            email="barna@gmail.Com",
            password=" "
        )

        response = self.tester.post(
                'api/v1/signup',
                content_type='application/json',
                data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(
            reply["message"], "Sorry, you did not enter your password!"
            )

    def test_password_length_below_6(self):
        user = dict(
            username="Barna",
            email="barna@gmail.com",
            password="1Bbar"
        )

        response = self.tester.post(
                'api/v1/signup',
                content_type='application/json',
                data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(
            reply["message"], "Passwords should be at least 6 characters long!"
            )

    def test_password_correct(self):
        user = dict(
            username="Barna",
            email="barna@gmail.com",
            password="12Byi567"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"], "Barna has registered successfully")

    def test_user_login_empty_username(self):
        user = dict(
            username='',
            password='aoixamklx'
        )

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'You did not enter your username!')

    def test_user_login_space_username(self):
        user = dict(
            username=' ',
            password='aoixamklx'
        )

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'You did not enter your username!')

    def test_user_login_empty_password(self):
        user = dict(
            username='Barna',
            password=''
        )

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'You did not enter your password!')

    def test_user_login_space_password(self):
        user = dict(
            username='Barna',
            password=' '
        )

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'You did not enter your password!')

    def test_user_login_successfully(self):
        """Test user can login successfully"""
        user = dict(
            username='username',
            email='username@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'username is logged in.')

    def tearDown(self):
        self.db.drop_user_table()
