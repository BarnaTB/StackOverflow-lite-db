import unittest
import json
from api.models import Answer
from api import app
from database.db import DbConnection


class TestAnswer(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DbConnection()

    def test_add_answer_without_question(self):
        """Test that a user cannot add answer to non-existent question"""
        user1 = dict(
            username='barna',
            email='barna@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user1)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        self.assertEqual(reply['message'], 'barna is logged in.')

        answer = dict(
            answer=''
        )

        response = self.tester.post(
            'api/v1/questions/2/answers',
            content_type='application/json',
            data=json.dumps(answer),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        self.assertEqual(
            response.status_code, 400
        )

    def test_add_answer_without_details(self):
        """Test user cannot add an empty answer"""
        user1 = dict(
            username='username',
            email='username@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user1)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'username is logged in.')

        token = reply['token']

        question = dict(
            details="my question"
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        user2 = dict(
            username='barna',
            email='barna@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user2)
        )

        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user2)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        self.assertEqual(reply['message'], 'barna is logged in.')

        answer = dict(
            answer=''
        )

        response = self.tester.post(
            'api/v1/questions/2/answers',
            content_type='application/json',
            data=json.dumps(answer),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        self.assertEqual(
            response.status_code, 400
        )

    def test_add_answer_successfully(self):
        """
        Test user can add an answer successfully
        """
        user1 = dict(
            username='username',
            email='username@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user1)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'username is logged in.')

        token = reply['token']

        question = dict(
            question="my question"
        )

        response = self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        self.assertEqual(response.status_code, 201)

        user2 = dict(
            username='barna',
            email='barna@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user2)
        )

        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user2)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        self.assertEqual(reply['message'], 'barna is logged in.')

        answer = dict(
            answer='this is my answer'
        )

        response = self.tester.post(
            'api/v1/questions/1/answers',
            content_type='application/json',
            data=json.dumps(answer),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['Message'], 'Answer added succesfully!')

    def test_add_answer_to_question_which_does_not_exist(self):
        """
        Test that a user can't add an answer to a question which does not exist
        """
        user1 = dict(
            username='username',
            email='username@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user1)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'username is logged in.')

        token = reply['token']

        question = dict(
            details="my question"
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        user2 = dict(
            username='barna',
            email='barna@mail.com',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user2)
        )

        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user2)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        self.assertEqual(reply['message'], 'barna is logged in.')

        answer = dict(
            answer='this is my answer'
        )

        response = self.tester.post(
            'api/v1/questions/2/answers',
            content_type='application/json',
            data=json.dumps(answer),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        self.assertEqual(
            response.status_code, 400
        )

    def tearDown(self):
        self.db.drop_user_table()
        self.db.drop_questions_table()
        self.db.drop_answers_table()
