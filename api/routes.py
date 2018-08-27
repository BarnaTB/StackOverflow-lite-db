from flask import Flask, request, jsonify
import uuid
import json
from api.models import Answer, Question, User, questions, users, answers
from flask import Blueprint
import re
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api.db import DbConnection

db = DbConnection()


mod = Blueprint('questions', __name__)


@mod.route('/questions', methods=['POST'])
@jwt_required
def add_question():
    """
    Function enables user to create a question by first checking if they have
    entered an empty string and returns an error message in that case. If not,
    it creates a question with the information from the json object and adds
    the question to a list of qeustions called 'questions' and returns a
    success message wuth the question that has been created.
    """
    data = request.get_json()

    details = data.get('details')

    if not details or details.isspace():
        return jsonify({
            "message": "Sorry, you didn't enter any question!"
        }), 400
    userId = get_jwt_identity()
    question = Question(user_id, details)
    db.insert_question(user_id, details)
    # questions.append(question)

    return jsonify({
        # "id": db.fetch_questionId(details),
        "question": question.__dict__,
        "message": "Question added successfully!"
    }), 201


@mod.route('/questions', methods=['GET'])
@jwt_required
def get_all_questions():
    """
    Function enables a user to fetch all questions on the platform by checking
    if the length of the questions list is not zero, in which case it returns
    an error message telling the user there are no questions in the list yet
    else, it returns all the questions in the list of questions on the
    platform.
    """
    user_id = get_jwt_identity()

    if Question.fetch_all_questions() is None:
        return jsonify({
            'message': 'Sorry there are no questions yet!'
        }), 404
    questions = db.fetch_questions(user_id)
    if questions:
        return jsonify({
            'Questions': questions,
            'message': 'Questions fetched successfully!'
        }), 200
    return jsonify({
        'message': 'There are no questions for this user yet!'
    }), 404


@mod.route('/questions/<int:questionId>/answers', methods=['POST'])
@jwt_required
def add_answer(questionId):
    """
    Function enables user to add an answer to a question on the platform.
    Checks if there is an empty string and returns a message telling the
    user that they didn't enter anything. Also checks if there are any
    questions in the list and if not returns a message that there are not
    questions yet.
    Then checks if the question whose id they entered exists and if not,
    returns a message that the quetion does not exist else, returns the
    answer the user entered together with the question.

    :param questionId:
    Parameter holds the id of the question that the user wishes to answer.
    """
    data = request.get_json()

    details = data.get('details')
    answerId = len(answers)

    answerId += 1

    try:
        if not details or details.isspace():
            return jsonify({
                'message': 'Sorry, you did not enter any answer!'
            }), 400
        if len(questions) == 0:
            return jsonify({
                'message': 'Sorry, there are no questions yet!!'
            }), 400

        question = questions[questionId - 1]
        answer = Answer(questionId, answerId, details)
        answers.append(answer)

        return jsonify({
            'Question': question.__dict__,
            'Answer': answer.__dict__,
            'Message': 'Answer added succesfully!'
        }), 201
    except IndexError:
        return jsonify({
            'message': 'Question does not exist.'
        }), 404


@mod.route('/questions/<int:questionId>', methods=['GET'])
@jwt_required
def get_one_question(questionId):
    """
    Function enables a user to fetch a single question from the platform
    using the questionId by checking if that id corresponds to any
    question in the list in which case it returns a success message
    with the question that has been fetched. In a case where the question
    id does not match, an error message is returned stating that the
    question does not exist.

    :param questionId:
    Parameter holds an integer value of the question id which is the id
    of the question that the user user to fetch.
    """
    try:
        if len(questions) < 0:
            return jsonify({
                'message': 'You have no questions yet.'
            }), 400
        question = questions[questionId - 1]
        # ans = filter(lambda a: a['questionId'] == questionId, answers)
        return jsonify({
            'Answers': [answer.__dict__ for answer in answers if answer.questionId == questionId],
            'Question': question.__dict__,
            'Message': 'Question fetched successfully!'
        }), 200
    except IndexError:
        return jsonify({
            'message': 'Question does not exist.'
        }), 404


@mod.route('/questions/<int:questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId):
    try:
        if len(questions) == 0:
            return jsonify({
                'message': 'There are no questions to delete!'
            }), 400
        for question in questions:
            if questionId == question.questionId:
                questions.remove(question)
                return jsonify({
                    'message': 'Question deleted!'
                }), 200
    except IndexError:
        return jsonify({
            'message': 'Question does not exist.'
        }), 404


@mod.route('/signup', methods=['POST'])
def register():
    """
    Function enables user to register on the platform. It checks if all the
    required data is added by the user and then validates that data using
    regular expressions for the email and password. Returns username in case
    of successful registration.
    """
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    userId = uuid.uuid4()

    if not username or username.isspace():
        return jsonify({
            'message': 'Sorry, you did not enter your username!'
        }), 400
    if not email or email.isspace():
        return jsonify({
            'message': 'Sorry, you did not enter your email!'
        }), 400
    if not password or password.isspace():
        return jsonify({
            'message': 'Sorry, you did not enter your password!'
        }), 400
    # source: https://docs.python.org/2/howto/regex.html
    if not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
        return jsonify({
            'message': 'Invalid email address!'
        }), 400
    # source: https://docs.python.org/2/howto/regex.html
    low = re.search(r"[a-z]", password)
    up = re.search(r"[A-Z]", password)
    num = re.search(r"[0-9]", password)
    if not all((low, up, num)):
        return jsonify({
            'message': 'Include at least one of each of these characters(A-Za-z0-9)'
        }), 400
    if len(password) < 6:
        return jsonify({
            'message': 'Passwords should be at least 6 characters long!'
        }), 400
    if db.fetch_username(username):
        return jsonify({
            'message': 'Sorry, that username is registered to another user!'
        }), 400
    if db.fetch_user_email(email):
        return jsonify({
            'message': 'Sorry, that email is registered to another user!'
        }), 400
    user = User(userId, username, email, password)
    # hashed_password = user.generate_hash()
    db.insert_user(userId, username, email, password)
    users.append(user)

    return jsonify({
        'Username': user.username,
        'message': '{} has registered successfully'.format(username)
    }), 400


@mod.route('/login', methods=['POST'])
def login():
    """
    Function enables to login after validating the data they entered.
    Returns a success message with the username in case of successful login.
    """
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or username.isspace():
        return jsonify({
            'message': 'You did not enter your username!'
        }), 400
    if not password or password.isspace():
        return jsonify({
            'message': 'You did not enter your password!'
        }), 400
    if not db.fetch_username(username):
        return jsonify({
            'message': 'Sorry, wrong username!'
        }), 400
    if not db.fetch_user_password(username):
        return jsonify({
            'message': 'Sorry, wrong password!'
        }), 400
    userId = db.fetch_userId(username)
    access_token = create_access_token(userId)
    return jsonify({
        'token': access_token,
        'message': '{} is logged in.'.format(username)
    }), 200
