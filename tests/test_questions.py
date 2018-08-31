import unittest
import psycopg2
import pprint
import json
from api.models import Question
from api import app
from database.db import DbConnection


class TestQuestions(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.tester = app.test_client(self)
        db = DbConnection()
        db.create_questions_table()
        self.user1 = dict(
            username='barna',
            email='barna@email.com',
            password='Pwer52j'
        )
        self.user2 = dict(
            username='barna',
            password='Pwer52j'
        )

    def test_add_question(self):
        signup_response = self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user1))

        self.assertEqual(signup_response.json, {"message": "User created successfully!"})
        self.assertEqual(signup_response.status_code, 201)

        login_response = self.tester.post(
            'api/v1/auth/login', content_type="application/json", data=json.dumps(user2))
        self.assertEqual(login_response.status_code, 200)

        login = login_response.json
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
        # reply = json.loads(response.data.decode())

        self.assertEqual(response.data, "Question added successfully!")

    def test_add_question_empty_string(self):
        question = dict(
            question=''
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"], "Sorry, you didn't enter any question!")

    def test_add_question_user_enters_a_space(self):
        question = dict(
            question=' '
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"], "Sorry, you didn't enter any question!")

    def test_get_one_question(self):
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

        self.assertEqual(response.status_code, 200)

    def test_get_one_question_if_there_are_no_questions_yet(self):
        response = self.tester.get(
            'api/v1/questions/1'
        )

        if len(questions) < 0:
            self.assertEqual(
                response['message'], 'You have no questions yet.'
                )

    def test_get_one_question_out_of_index(self):
        question = dict(
            question='my question'
        )

        self.tester.post(
            'api/v1/questions',
            content_type='applcation/json',
            data=json.dumps(question)
        )

        response = self.tester.get(
            'api/v1/questions/2'
        )

        if len(questions) == 1:
            # self.assertEqual(
            #     response['message'], 'Question does not exist.'
            #     )
            self.assertRaises(IndexError, response)

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

    def test_delete_question(self):
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

        self.assertEqual(response.status_code, 200)

    # def test_delete_question_which_does_not_exist(self):
    #     question = dict(
    #         details='my question'
    #     )

    #     self.tester.post(
    #         'api/v1/questions',
    #         content_type='application/json',
    #         data=json.dumps(question)
    #     )

    #     response = self.tester.delete(
    #         'api/v1/questions/3'
    #     )

    #     if len(questions) == 1:
    #         self.assertEqual(response.status_code, 404)

    # def test_delete_questions_from_empty_list(self):
    #     response = self.tester.get(
    #         'api/v1/questions/1'
    #     )

    #     if len(questions) < 0:
    #         self.assertEqual(
    #             response['message'], 'There are no questions to delete!'
    #             )
