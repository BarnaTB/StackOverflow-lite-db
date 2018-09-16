from flask import jsonify
import re
from passlib.hash import pbkdf2_sha256 as sha256
from database.db import DbConnection
# from instance.config import DevelopmentConfig


users = []
questions = []
answers = []

db = DbConnection('test_db')


class User:
    def __init__(self, userId, username, email, password):
        self.userId = userId
        self.username = username
        self.email = email
        self.password = password

    def generate_hash(self):
        return sha256.hash(self.password)

    @staticmethod
    def verify_hash(password, password_hash):
        return sha256.verify(password, password_hash)

    @staticmethod
    def verify_password(username, password):
        user_password = db.fetch_user_password(username)
        user_pass = user_password[0][0]
        if user_pass == password:
            return True
        return False


class Question:
    def __init__(self, user_id, details):
        self.user_id = user_id
        # self.questionId = questionId
        self.details = details

    @staticmethod
    def fetch_all_questions():
        qn = db.fetch_all_questions()
        if qn is None:
            return None
        return qn

    @staticmethod
    def fetch_one_user_question(user_id, question_id):
        qn = db.fetch_one_user_question(user_id, question_id)
        if qn is None:
            return None
        return qn

    @staticmethod
    def fetch_answers(question_id):
        ans = db.fetch_answers_by_question_id(question_id)
        if ans is None:
            return False
        return ans

    @staticmethod
    def fetch_question_by_id(question_id):
        qn = db.fetch_question_by_id(question_id)
        if qn is None:
            return None
        return qn

    @staticmethod
    def fetch_user_questions(user_id, question_id):
        qns = db.fetch_user_questions(user_id, question_id)
        if qns is None:
            return None
        return qns

    def update_question(self, question_id, details):
        db.update_question(self.user_id, question_id, details)

        qn = db.fetch_user_questions(self.user_id, question_id)

        return qn


class Answer:
    def __init__(self, user_id, question_id, answer_id, details):
        self.answerId = answer_id
        self.question_id = question_id
        self.details = details
        self.user_id = user_id
        self.accepted = False

    @staticmethod
    def fetch_answers(question_id):
        ans = db.fetch_answers_by_question_id(question_id)
        if ans is None:
            return None
        return ans
