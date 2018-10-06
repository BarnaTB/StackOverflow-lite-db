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

    def validate_username(self):
        """
        Method to validate the username entered by the user.

        :returns:
        True - if the username is valid.

        False - if the username is invalid.
        """
        if self.username == '' or self.username.isspace() or (not isinstance(
                self.username, str)):
            return False
        else:
            return True

    def validate_email(self):
        """
        Method to validate the email entered by a user.

        :returns:
        True - if the email is valid.

        False - if the email is invalid.
        """
        if self.email == '' or self.email.isspace() or (not isinstance(
                self.email, str)) or (not re.match(
                    r"[^@.]+@[A-Za-z]+\.[a-z]+", self.email)):
                    # source: https://docs.python.org/2/howto/regex.html
            return False
        else:
            return True

    def validate_password(self):
        """
        Method to validate the password entered by a user.

        :returns:
        True - if the password is valid.

        False - if the password is invalid
        """
        low = re.search(r"[a-z]", self.password)
        up = re.search(r"[A-Z]", self.password)
        num = re.search(r"[0-9]", self.password)
        if self.password == '' or self.password.isspace() or (not isinstance(
                self.password, str)) or not all((low, up, num)) or len(
                    self.password) < 6:
            return False
        else:
            return True

    def add_user(self):
        """Method to register a new user in the database."""
        hashed_password = self.generate_hash()
        db.insert_user(self.username, self.email, hashed_password)

    def generate_hash(self):
        return sha256.hash(self.password)

    @staticmethod
    def verify_hash(password, password_hash):
        return sha256.verify(password, password_hash)

    @staticmethod
    def verify_password(username, password):
        user_password = db.fetch_user_password(username)
        user_pass = user_password[0][0]
        if not User.verify_hash(password, user_pass):
            return False
        return True


class Question:
    questions = []
    answers = []

    def __init__(self, question):
        self.question = question

    @staticmethod
    def fetch_all_questions():
        qn = db.fetch_all_questions()
        if qn is None or qn == []:
            return None
        return qn

    @staticmethod
    def fetch_one_user_question(user_id, question_id):
        qn = db.fetch_one_user_question(user_id, question_id)
        if qn is None or qn == []:
            return None
        else:
            question = {}
            question['question_id'] = qn[0][1]
            question['question'] = qn[0][2]

            return question

    @staticmethod
    def fetch_answers(question_id):
        ans = db.fetch_answers_by_question_id(question_id)
        if ans is None or ans == []:
            return False
        for answer in ans:
            answer_dict = {}
            print(answer)
            answer['answerid'] = answer[2]
            answer['answer'] = answer[3]
            answer['accepted'] = answer[4]

            answers.append(answer_dict)
        return answers

    @staticmethod
    def fetch_question_by_id(question_id):
        qn = db.fetch_question_by_id(question_id)
        if qn is None or qn == []:
            return None
        else:
            question = {}
            question['userid'] = qn[0][0]
            question['questionid'] = qn[0][1]
            question['details'] = qn[0][2]

            return question

    @staticmethod
    def fetch_user_questions(user_id, question_id):
        qns = db.fetch_user_questions(user_id, question_id)
        if qns is None or qns == []:
            return None
        else:
            question = {}
            question['user_id'] = qns[0][0]
            question['question_id'] = qns[0][1]
            question['details'] = qns[0][2]
            return question

    @staticmethod
    def update_question(user_id, question_id, question):
        db.update_question(user_id, question_id, question)

        qn = db.fetch_user_questions(user_id, question_id)
        dict_question = {}
        dict_question['userid'] = qn[0][0]
        dict_question['questionid'] = qn[0][1]
        dict_question['details'] = qn[0][2]
        return dict_question

    @staticmethod
    def fetch_questions(user_id):
        qns = db.fetch_questions(user_id)
        if qns is None or qns == []:
            return None
        for question in qns:
            question_dict = {}
            question_dict['question_id'] = question[1]
            question_dict['question'] = question[2]

            questions.append(question_dict)

        return questions


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
