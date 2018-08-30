import unittest
import json
from api.models import Answer
from api import app


class TestAnswer(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.tester = app.test_client(self)

    def test_add_answer_without_question(self):
        answer = dict(
            details="my answer"
        )

        response = self.tester.post(
            'api/v1/questions/1/answers',
            content_type='application/json',
            data=json.dumps(answer)
        )

        if len(questions) == 0:
            self.assertEqual(
                response.status_code, 404
                )
            self.assertRaises(IndexError, response)

    def test_add_answer_without_details(self):
        question = dict(
            details="my question"
        )

        answer = dict(
            details=""
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )

        response = self.tester.post(
            'api/v1/questions/1/answers',
            content_type='application/json',
            data=json.dumps(answer)
        )

        self.assertEqual(
            response.status_code, 400
            )

    def test_add_answer_with_both_answer_and_question_details(self):
        question = dict(
            details="my question"
        )

        answer = dict(
            details="my answer"
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )

        response = self.tester.post(
            'api/v1/questions/1/answers',
            content_type='application/json',
            data=json.dumps(answer)
        )

        self.assertEqual(
            response.status_code, 201
            )

    def test_add_answer_to_question_which_does_not_exist(self):
        question = dict(
            details="my question"
        )

        answer = dict(
            details="my answer"
        )

        self.tester.post(
            'api/v1/questions',
            content_type='application/json',
            data=json.dumps(question)
        )

        response = self.tester.post(
            'api/v1/questions/2/answers',
            content_type='application/json',
            data=json.dumps(answer)
        )

        if len(questions) == 1:
            self.assertEqual(
                response.status_code, 400
                )




class ModelsTests(unittest.TestCase):
    def test_user_model(self):
        user = User('1', 'Barna', 'barna@gmail.com', '12345')

    def test_question_model(self):
        question = Question('1', '2', 'what is coding?')

    def test_answer_model(self):
        answer = Answer('1', '2', 'coding is obulamu')