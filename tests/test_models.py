import unittest
from api.models import User, Question, Answer



class ModelsTests(unittest.TestCase):
    def test_user_model(self):
        user = User('1', 'Barna', 'barna@gmail.com', '12345')

    def test_question_model(self):
        question = Question('1', '2', 'what is coding?')

    def test_answer_model(self):
        answer = Answer('1', '2', 'coding is obulamu')
