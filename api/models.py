from api.db import DbConnection
from flask import jsonify
import re
from passlib.hash import pbkdf2_sha256 as sha256
from api.db import DbConnection

users = []
questions = []
answers = []

db = DbConnection()


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


class Question:
    def __init__(self, userId, details):
        self.userId = userId
        # self.questionId = questionId
        self.details = details

    @staticmethod
    def fetch_all_questions():
        qn = db.fetch_all_questions()
        if qn is None:
            return None
        return qn


class Answer:
    def __init__(self, questionId, answerId, details):
        self.answerId = answerId
        self.questionId = questionId
        self.details = details
