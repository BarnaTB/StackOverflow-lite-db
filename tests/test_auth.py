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
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'username has registered successfully')

    def test_registration_empty_username(self):
        """Test that a user cannot register with empty username"""
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
        """Test that a user cannot register with spaces for username"""
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
        """Test that a user cannot register with empty email"""
        user = dict(
            username="barna",
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
        """Test that a user cannot register when they enter spaces for email"""
        user = dict(
            username="barna",
            email=" ",
            password="123456"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"],
                         "Sorry, you did not enter your email!")

    def test_registration_email_vague_data(self):
        user = dict(
            username="barna",
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
        """Test a user cannot register with a empty password"""
        user = dict(
            username="barna",
            email="barna@gmail.Com",
            password=""
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"],
                         "Sorry, you did not enter your password!")

    def registration_password_spaces_entry(self):
        """Test a user cannot register with spaces for password"""
        user = dict(
            username="barna",
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
        """Tests a user cannot register with password length less than 6"""
        user = dict(
            username="barna",
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
        """Test user can login with correct password"""
        user = dict(
            username="barna",
            email="username@mail.com",
            password="12Byi567"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"],
                         "barna has registered successfully")

    def test_user_login_empty_username(self):
        """Test a user cannot login with empty username"""
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
        """Test a user cannot login with spaces entry in the username"""
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
        """Test a user cannot login with empty password"""
        user = dict(
            username='barna',
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
        """Test a user cannot login with spaces for password"""
        user = dict(
            username='barna',
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
            username='barna',
            email='username@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/signup',
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

        self.assertIn(reply['token'], reply['token'])

    def tearDown(self):
        self.db.drop_user_table()
        self.db.drop_questions_table()
        self.db.drop_answers_table()
