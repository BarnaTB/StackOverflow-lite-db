import unittest
import psycopg2
import pprint
import json
from api.models import Question
from api import app
from database.db import DbConnection


class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DbConnection()

    def test_add_question_successfully(self):
        """Method to test that a user can add a question successfully"""
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

        login_user = dict(
            username='username',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(login_user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'username is logged in.')
        login = response.json
        token = login['token']

        question = dict(
            question='what is code?'
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(token)},
            data=json.dumps(question)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], "Question added successfully!")

    def test_add_question_empty_string(self):
        """Method to test that a user cannot post empty question"""

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

        login_user = dict(
            username='username',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(login_user)
        )

        reply = json.loads(response.data.decode())
        
        self.assertEqual(reply['message'], 'username is logged in.')
        token = reply['token']

        question = dict(
            question=''
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(
            reply["message"], "Sorry, you didn't enter any question!"
        )

    def test_add_question_user_enters_a_space(self):
        """Method to test that a user cannot add a question with empty space"""
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

        login_user = dict(
            username='username',
            password='tyIY790hskj'
        )

        response = self.tester.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(login_user)
        )

        reply = json.loads(response.data.decode())

        question = dict(
            question=' '
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(
            reply["message"], "Sorry, you didn't enter any question!"
        )

    def test_get_one_question_without_token(self):
        question = dict(
            question='this is my question'
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        response = self.tester.get(
            'api/v1/questions/1'
        )

        self.assertEqual(response.status_code, 401)

    # def test_get_one_question_out_of_index(self):
    #     question = dict(
    #         question='my question'
    #     )

    #     self.tester.post(
    #         'api/v1/questions',
    #         content_type='applcation/json',
    #         data=json.dumps(question)
    #     )

    #     response = self.tester.get(
    #         'api/v1/questions/2'
    #     )

    #     self.assertEqual(, response)

    def test_get_all_questions(self):
        question = dict(
            question='my question'
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )

        response = self.tester.get(
            'api/v1/questions'
        )

        self.assertEqual(
            response.status_code, 200
        )

    # def test_get_all_questions_from_empty_list(self):
    #     response = self.tester.get(
    #         'api/v1/questions/1'
    #     )

    #     if len(questions) < 0:
    #         self.assertEqual(
    #             response['message'], 'You have no questions yet.'
    #             )

    def test_delete_question_without_token(self):
        question = dict(
            details='my question'
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )

        response = self.tester.delete(
            'api/v1/questions/1'
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_question_which_does_not_exist(self):
        question = dict(
            details='my question'
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )

        response = self.tester.delete(
            'api/v1/questions/3'
        )

        if len(questions) == 1:
            self.assertEqual(response.status_code, 404)

    def test_delete_questions_from_empty_list(self):
        response = self.tester.get(
            'api/v1/questions/1'
        )

        if len(questions) < 0:
            self.assertEqual(
                response['message'], 'There are no questions to delete!'
            )

    def tearDown(self):
        self.db.drop_user_table()
        self.db.drop_questions_table()
