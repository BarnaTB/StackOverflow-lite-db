import psycopg2
import os
from pprint import pprint


class DbConnection:
    def __init__(self):
        if os.getenv('APP_SETTINGS') == 'testing':
            self.dbname = 'test_db'
        else:
            self.dbname = 'stackoverflow'
        try:
            self.connection = psycopg2.connect(
                database=self.dbname,
                user='postgres',
                password='##password',
                host='localhost',
                port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users\
                    (userid SERIAL PRIMARY KEY, username TEXT NOT NULL,\
                    email TEXT NOT NULL, password TEXT NOT NULL)
                    """
            )
            self.cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS questions\
                    (userid INTEGER NOT NULL, questionid SERIAL PRIMARY KEY,\
                    question TEXT NOT NULL);
                    """
            )
            self.cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS answers\
                    (userid INTEGER NOT NULL, questionid INTEGER NOT NULL,\
                    answerid SERIAL PRIMARY KEY, answer TEXT NOT NULL,\
                    accepted BOOL DEFAULT FALSE);
                    """
            )

            pprint("Connected!")
            pprint(self.dbname)
        except Exception as e:
            pprint(e)
            pprint('Failed to connect to database!')

    def insert_user(self, username, email, password):
        insert_user_command = """
        INSERT INTO users(username, email, password) VALUES('{}', '{}', '{}');
        """.format(username, email, password)
        self.cursor.execute(insert_user_command)

    def fetch_user(self, username):
        fetch_username_command = """
        SELECT * FROM users WHERE username='{}';
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

    def fetch_userId(self, username):
        fetch_userId = """
        SELECT userId FROM users WHERE username='{}';
        """.format(username)
        self.cursor.execute(fetch_userId)
        user = self.cursor.fetchone()

        return user

    def insert_question(self, user_id, question):
        insert_question_command = """
        INSERT INTO questions (userId, question) VALUES(%s, %s);
        """
        self.cursor.execute(
            insert_question_command, [user_id, question]
        )

    def fetch_question_by_id(self, question_id):
        fetch_question_id_command = """
        SELECT * FROM questions WHERE questionid='{}'
        """.format(question_id)
        self.cursor.execute(fetch_question_id_command)
        question = self.cursor.fetchall()

        return question

    def fetch_questions(self, user_id):
        fetch_questions_command = """
        SELECT * FROM questions WHERE userid=%s
        """
        self.cursor.execute(fetch_questions_command, [user_id])
        questions = self.cursor.fetchall()

        return questions

    def fetch_all_questions(self):
        fetch_all_questions_command = """
        SELECT * FROM  questions;
        """
        self.cursor.execute(fetch_all_questions_command)
        questions = self.cursor.fetchall()

        return questions

    def fetch_one_question(self, user_id, question_id):
        fetch_questions_command = """
        SELECT * FROM questions WHERE userid=%s AND questionid=%s;
        """
        self.cursor.execute(
            fetch_questions_command, [user_id, question_id]
        )
        qns = self.cursor.fetchall()

        return qns

    def delete_question(self, user_id, question_id):
        delete_question_command = """
        DELETE FROM questions WHERE userid=%s AND questionid=%s;
        """
        self.cursor.execute(
            delete_question_command, [user_id, question_id]
        )

    def insert_answer(self, user_id, question_id, answer):
        insert_answer_command = """
        INSERT INTO answers(userid, questionid, answer) VALUES(%s, %s, %s);
        """
        self.cursor.execute(
            insert_answer_command, [user_id, question_id, answer]
        )

    def fetch_answers_by_question_id(self, question_id):
        fetch_answer_command = """
        SELECT * FROM answers WHERE questionid='{}'
        """.format(question_id)
        self.cursor.execute(fetch_answer_command)
        ans = self.cursor.fetchall()

        return ans

    def fetch_answers_by_user_id(self, user_id, question_id, answer_id):
        fetch_answer_command = """
        SELECT * FROM answers WHERE userid='{}' AND questionid='{}' AND \
answerid='{};'
        """.format(user_id, question_id, answer_id)
        self.cursor.execute(fetch_answer_command)
        ans = self.cursor.fetchall()

        return ans

    def delete_answer(self, user_id, question_id):
        delete_answer_command = """
        DELETE FROM answers WHERE userid='{}' AND questionid='{}';
        """.format(user_id, question_id)
        self.cursor.execute(delete_answer_command)

    def delete_all_answers(self, question_id):
        delete_all_answers_command = """
        DELETE FROM answers WHERE questionid='{}';
        """.format(question_id)
        self.cursor.execute(delete_all_answers_command)

    def accept_answer(self, question_id, answer_id):
        prefer_answer_command = """
        UPDATE answers SET accepted=%s \
WHERE questionid=%s AND answerid=%s;
        """
        self.cursor.execute(
            prefer_answer_command, [True, question_id, answer_id]
        )

    def update_question(self, user_id, question_id, question):
        update_question_command = """
        UPDATE questions SET question=%s \
WHERE userid=%s AND questionid=%s;
        """
        self.cursor.execute(
            update_question_command, [question, user_id, question_id]
        )

    def update_answer(self, user_id, answer_id, answer):
        update_answer_command = """
        UPDATE answers SET answer=%s \
WHERE userid=%s AND questionid=%s;
        """
        self.cursor.execute(
            update_answer_command, [answer, user_id, answer_id]
        )

    def drop_table(self, table_name):
        drop_table_command = """
        DROP TABLE {};
        """.format(table_name)
        self.cursor.execute(drop_table_command)
