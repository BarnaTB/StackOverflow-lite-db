from flask import Flask, request, jsonify, Blueprint
from api.models import Answer, Question, User, questions, users, answers
import re
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from database.db import DbConnection
from flasgger import swag_from


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

    question = data.get('question')

    if not question or question.isspace():
        return jsonify({
            "message": "Sorry, you didn't enter any question!"
        }), 400
    user_id = get_jwt_identity()
    db.insert_question(user_id, question)

    return jsonify({
        "question": question,
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
        for question in questions:
            question_dict = {}
            question_dict['questionid'] = question[1]
            question_dict['question'] = question[2]
            return jsonify({
                'Questions': question_dict,
                'message': 'Questions fetched successfully!'
            }), 200
    return jsonify({
        'message': 'There are no questions for this user yet!'
    }), 404


@mod.route('/questions/<int:question_id>', methods=['GET'])
@jwt_required
def get_one_question(question_id):
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
    user_id = get_jwt_identity()
    qn = Question.fetch_one_user_question(user_id, question_id)
    ans = Question.fetch_answers(question_id)
    if qn:
        question = {}
        question['question_id'] = qn[0][1]
        question['details'] = qn[0][2]
        if not ans:
            return jsonify({
                'Answers': 'Sorry, this question has no answers yet!',
                'Question': question,
                'Message': 'Question fetched successfully!'
            }), 200
        for answer in ans:
            answer_dict = {}
            answer['answerid'] = answer[2]
            answer['answer'] = answer[3]
            answer['accepted'] = answer[4]
            return jsonify({
                'Answers': answer_dict,
                'Question': question,
                'Message': 'Question and answers fetched successfully!'
            })
    return jsonify({
            'message': 'Sorry, that question does not exist!'
        }), 400


@mod.route('/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required
def add_answer(question_id):
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

    answer = data.get('answer')

    user_id = get_jwt_identity()
    if not answer or answer.isspace():
        return jsonify({
            'message': 'Sorry, you did not enter any answer!'
        }), 400
    questions = Question.fetch_all_questions()
    if len(questions) == 0:
        return jsonify({
            'message': 'Sorry, there are no questions yet!'
        }), 400

    qn = Question.fetch_question_by_id(question_id)
    if qn:
        question = {}
        question['userid'] = qn[0][0]
        question['questionid'] = qn[0][1]
        question['details'] = qn[0][2]

        db.insert_answer(user_id, question_id, answer)

        return jsonify({
            'Question': question,
            'Answer': answer,
            'Message': 'Answer added succesfully!'
        }), 201
    return jsonify({
        'message': 'Sorry, this question does not exist!'
    }), 404


@mod.route('/questions/<int:question_id>', methods=['DELETE'])
@jwt_required
def delete_question(question_id):
    """
    Function enables a logged in user delete a question they created on the
    platform. Checks if there are any questions in the database and returns
    an appropriate error message if this is false, else checks that the user
    is the creator of the question and if that question is existent in the
    database and then the user is allowed to deleted the question.

    :param question_id:
    Holds the integer value of the question that the user wishes to delete
    from the database.

    :returns:
    A success message when the question is succesfully deleted.
    """
    user_id = get_jwt_identity()
    questions = Question.fetch_all_questions()
    if len(questions) == 0:
        return jsonify({
            'message': 'There are no questions to delete!'
        }), 400
    question = Question.fetch_question_by_id(question_id)
    questions = Question.fetch_user_questions(user_id, question_id)
    answers = Answer.fetch_answers(question_id)
    if questions:
        db.delete_question(user_id, question_id)
        if answers:
            return jsonify({
                'message': 'Question and answers deleted!'
            }), 200
        return jsonify({
            'message': 'Question deleted!'
        }), 200
    if question:
        return jsonify({
            'message': 'Sorry, you cannot delete a question that does not \
belong to you!'
        }), 400
    return jsonify({
        'message': 'Sorry, this question does not exist!'
    }), 404


@mod.route('/<int:question_id>', methods=['PUT'])
@jwt_required
def modify_question(question_id):
    data = request.get_json()

    question = data.get('question')

    user_id = get_jwt_identity()

    if not question or question.isspace():
        return jsonify({
            "message": "Sorry, you didn't enter any question!"
        }), 400
    question = Question.fetch_question_by_id(question_id)
    questions = Question.fetch_user_questions(user_id, question_id)
    if questions:
        if question:
            updated_question = qn.update_question(question_id, question)
            dict_question = {}
            dict_question['userid'] = updated_question[0][0]
            dict_question['questionid'] = updated_question[0][1]
            dict_question['details'] = updated_question[0][2]
            return jsonify({
                "question": dict_question,
                "message": "Question added successfully!"
            }), 201
        return jsonify({
            'message': 'Sorry, this question does not exist!'
        }), 404
    return jsonify({
        'message': 'Sorry, you have no questions to modify!'
    }), 404


@mod.route('/questions/<question_id>/answers/<answer_id>', methods=['PUT'])
@jwt_required
def accept_answer(question_id, answer_id):
    data = request.get_json()

    accepted = data.get('accepted')

    user_id = get_jwt_identity()
    qn = Question.fetch_user_questions(user_id, question_id)
    ans = Question.fetch_answers(question_id)
    if qn:
        question = {}
        question['user_id'] = qn[0][0]
        question['question_id'] = qn[0][1]
        question['details'] = qn[0][2]
        if not ans:
            return jsonify({
                'Answers': 'Sorry, this question has no answers yet!',
                'Question': question,
                'Message': 'Answers to this question were not found!'
            }), 404
        db.accept_answer(question_id, answer_id, accepted)
        accepted_answer = Answer.fetch_answers(question_id)
        return jsonify({
            'Answer': accepted_answer,
            'Question': question,
            'Message': 'Answer updated successfully!'
        }), 200
    else:
        return jsonify({
                'message': 'Sorry, that question does not exist!'
            }), 404


@mod.route('/signup', methods=['POST'])
@swag_from('docs/register.yml')
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
    low = re.search(r"[a-z]", password)
    up = re.search(r"[A-Z]", password)
    num = re.search(r"[0-9]", password)
    if not all((low, up, num)):
        return jsonify({
            'message': 'Passwords should include lower case,\
upper case and numbers'
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
    # hashed_password = generate_password_hash(password)
    user = User(username, email, password)
    user.add_user()

    return jsonify({
        'Username': username,
        'message': '{} has registered successfully'.format(username)
    }), 201


@mod.route('/login', methods=['POST'])
@swag_from('docs/login.yml')
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
    if not User.verify_password(username, password):
        return jsonify({
            'message': 'Sorry, wrong password!'
        }), 400
    user_id = db.fetch_userId(username)
    access_token = create_access_token(user_id)
    return jsonify({
        'token': access_token,
        'message': '{} is logged in.'.format(username)
    }), 200
