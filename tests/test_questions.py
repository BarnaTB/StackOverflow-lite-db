import unittest
import json
from api.models import Question
from api import app


class TestQuestions(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.tester = app.test_client(self)

        self.login_data = {
            "username": "barna",
            "password": "ba25Th7"
        }

    def test_add_question(self):
        question = dict(
            details='details'
        )
        response = self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["message"], "Question added successfully!")

    def test_add_question_empty_string(self):
        question = dict(
            details=''
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
            details=' '
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
            details='this is my question'
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        response = self.tester.get(
            'api/v1/questions/1',
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
            details='my question'
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
            details='my question'
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

    def test_get_all_questions_from_empty_list(self):
        response = self.tester.get(
            'api/v1/questions/1'
        )

        if len(questions) < 0:
            self.assertEqual(
                response['message'], 'You have no questions yet.'
                )

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
        db = DbConnection()
        db.truncate_table('questions')
