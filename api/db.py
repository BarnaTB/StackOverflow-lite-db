import psycopg2
from pprint import pprint


class DbConnection:
    try:
        def __init__(self):
            self.connection = psycopg2.connect(
                "dbname='stackoverflow' user='postgres' password='##password' host='localhost' port='5432'"
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            pprint("Connected!")
    except:
        pprint('Failed to connect to database')

    def insert_user(self, userId, username, email, password):
        insert_user_command = """
        INSERT INTO users VALUES('{}', '{}', '{}', '{}');
        """.format(userId, username, email, password)
        self.cursor.execute(insert_user_command)

    def fetch_username(self, username):
        fetch_username_command = """
        SELECT username FROM users WHERE username='{}';
        """.format(username)
        self.cursor.execute(fetch_username_command)
        username = self.cursor.fetchone()

        return username

    def fetch_user_email(self, email):
        fetch_user_email_command = """
        SELECT email FROM users WHERE email='{}';
        """.format(email)
        self.cursor.execute(fetch_user_email_command)
        email = self.cursor.fetchone()

        return email

    def fetch_user_password(self, username):
        fetch_user_password_command = """
        SELECT password FROM users WHERE username='{}';
        """.format(username)
        self.cursor.execute(fetch_user_password_command)
        user = self.cursor.fetchall()

        return user

    def fetch_userId(self, username):
        fetch_userId = """
        SELECT userId FROM users WHERE username='{}';
        """.format(username)
        self.cursor.execute(fetch_userId)
        user = self.cursor.fetchone()

        return user

    def fetch_user(self, username):
        fetch_user_command = """
        SELECT * FROM users WHERE username='{}'
        """.format(username)
        self.cursor.execute(fetch_user_command)
        user = self.cursor.fetchall()

        return user

    def insert_question(self, user_id, details):
        insert_question_command = """
        INSERT INTO questions (userId, details) VALUES(%s, %s);
        """
        self.cursor.execute(insert_question_command, [user_id[0], details])

    def fetch_questionId(self, details):
        fetch_questionId_command = """
        SELECT questionId FROM questions WHERE details='{}'
        """.format(details)
        questionId = self.cursor.execute(fetch_questionId_command)

        return questionId

    def fetch_questions(self, user_id):
        fetch_questions_command = """
        SELECT * FROM questions WHERE userid=%s
        """
        self.cursor.execute(fetch_questions_command, [user_id[0]])
        questions = self.cursor.fetchall()

        return questions

    def fetch_all_questions(self):
        fetch_all_questions_command = """
        SELECT * FROM  questions;
        """
        self.cursor.execute(fetch_all_questions_command)
        questions = self.cursor.fetchall()

        return questions

    def fetch_user_questions(self, userId):
        fetch_questions_command = """
        SELECT * FROM questions WHERE userId='{}';
        """.format(userId)
        self.cursor.execute(fetch_questions_command)
        qns = self.cursor.fetchall()

        return qns

    def fetch_one_question(self, userId, questionId):
        fetch_one_question_command = """
        SELECT userId, questionId, question.details, answer.details FROM question, answer WHERE userId='{}' AND answer.questionId='{}';
        """.format(userId, questionId)
        self.cursor.execute(fetch_one_question_command)
        qn = self.cursor.fetchall()

        return qn

    def delete_question(self, userId, questionId):
        delete_question_command = """
        DELETE FROM questions WHERE userId='{}' AND questionId='{}';
        """.format(userId, questionId)
        self.cursor.execute(delete_question_command)

    def insert_answer(self, userId, questionId, details):
        insert_answer_command = """
        INSERT INTO answers(userId, questionId, details) VALUES('{}', '{}', '{}');
        """.format(userId, questionId, details)
        self.cursor.execute(insert_answer_command)

    def delete_answer(self, userId, questionId):
        delete_answer_command = """
        DELETE FROM answers WHERE userId='{}' AND questionId='{}';
        """.format(userId, questionId)
        self.cursor.execute(delete_answer_command)

    def prefer_answer(self, userId, questionId):
        prefer_answer_command = """
        UPDATE answers SET preference='Preferred' WHERE userId='{}' AND questionId='{}';
        """.format(userId, questionId)
        self.cursor.execute(prefer_answer_command)
