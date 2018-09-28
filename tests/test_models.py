import unittest
from api.models import User, Question, Answer


class TestModels(unittest.TestCase):
    def test_user_model(self):
        user = User('Barna', 'barna@gmail.com', '12345')

    def test_question_model(self):
        question = Question('what is coding?')

    def test_answer_model(self):
        answer = Answer('1', '2', '3', 'coding is obulamu')
