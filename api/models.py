from flask import jsonify
import re
from passlib.hash import pbkdf2_sha256 as sha256
from database.db import DbConnection


users = []
questions = []
answers = []

db = DbConnection()


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def add_user(self):
        db.insert_user(self.username, self.email, self.password)

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
    def __init__(self, question):
        self.question = question

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

    @staticmethod
    def update_question(user_id, question_id, question):
        db.update_question(user_id, question_id, question)

        qn = db.fetch_user_questions(user_id, question_id)

        return qn


class Answer:
    def __init__(self, user_id, question_id, answer_id, answer):
        self.answerId = answer_id
        self.question_id = question_id
        self.answer = answer
        self.user_id = user_id
        self.accepted = False

    @staticmethod
    def fetch_answers(question_id):
        ans = db.fetch_answers_by_question_id(question_id)
        if ans is None:
            return None
        return ans
