from flask import Flask, request, jsonify, Blueprint
from api.models import Answer, Question, User, questions, users, answers
import re
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from database.db import DbConnection
from flasgger import swag_from


db = DbConnection()


mod = Blueprint('questions', __name__)


@mod.errorhandler(404)
def page_not_found(e):
    return 'The page you are trying to access was not found!'


@mod.route('/signup', methods=['POST'])
@swag_from('docs/register.yml')
def register():
    """
    Function enables user to register on the platform.

    :returns:
    A success message when the user registers successfully.

    An error message in case of an unsuccessful registeration.
    """
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User(username, email, password)

    if not user.validate_username():
        return jsonify({
            'message': 'Sorry, you did not enter your username!'
        }), 400
    if not user.validate_email():
        return jsonify({
            'message': 'Sorry, your email cannot be empty and should \
be a valid email e.g(johndoe@example.com)!'
        }), 400
    if not user.validate_password():
        return jsonify({
            'message': 'Passwords cannot be empty and should include lower case, \
upper case and numbers and should be 6 characters or longer.'
        }), 400
    user_dict = User.fetch_user(username)
    if user_dict:
        return jsonify({
            'message': 'Sorry, that username is registered to another user!'
        }), 400
    if db.fetch_user_email(email):
        return jsonify({
            'message': 'Sorry, that email is registered to another user!'
        }), 400
    user.add_user()

    return jsonify({
        'message': '{} has registered successfully'.format(username)
    }), 201


@mod.route('/login', methods=['POST'])
@swag_from('docs/login.yml')
def login():
    """
    Function enables to login after validating the data they entered.

    :returns:
    A token which is used to access all other protected resources.
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
    user_dict = User.fetch_user(username)
    if not user_dict:
        return jsonify({
            'message': 'Sorry, wrong username!'
        }), 400
    if not User.verify_password(username, password):
        return jsonify({
            'message': 'Sorry, wrong password!'
        }), 400
    user = User.fetch_user(username)
    user_id = user['userid']
    access_token = create_access_token(user_id)
    return jsonify({
        'token': access_token
    }), 200


@mod.route('/questions', methods=['POST'])
@jwt_required
def add_question():
    """
    Function enables a logged in user to create a question. It creates a
    question with the information from the json object and adds the
    question to a database.

    :returns:
    A success message when the question is created successfully.

    An error message when the question is not created successfully.
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
    Function enables a logged in user to fetch all their questions on the
    platform.

    :returns:
    List - A list of questions created by the user on the platform.

    An error message in case there are no questions on the platform.
    """
    user_id = get_jwt_identity()

    if Question.fetch_all_questions() is None:
        return jsonify({
            'message': 'Sorry there are no questions yet!'
        }), 400
    qns = Question.fetch_questions(user_id)
    if qns is not None:
        return jsonify({
            'Questions': qns,
            'message': 'Questions fetched successfully!'
        }), 200
    return jsonify({
        'message': 'There are no questions for this user yet!'
    }), 400


@mod.route('/questions/<int:question_id>', methods=['GET'])
@jwt_required
def get_one_question(question_id):
    """
    Function enables a logged in user to fetch a single question from the
    platform.

    :params:
    question_id - holds an integer value of the unique id
    of the question that the user wishes to fetch.

    :returns:
    A single question whose id matches the parameter question_id.

    An error message in case the requested question does not exist.
    """
    user_id = get_jwt_identity()
    qn = Question.fetch_one_question(user_id, question_id)
    ans = Answer.fetch_answers(question_id)
    if qn is not None:
        if not ans:
            return jsonify({
                'Answers': 'Sorry, this question has no answers yet!',
                'Question': qn,
                'Message': 'Question fetched successfully!'
            }), 200
        return jsonify({
            'Answers': ans,
            'Question': qn,
            'Message': 'Question and answers fetched successfully!'
        })
    return jsonify({
        'message': 'Sorry, that question does not exist!'
    }), 400


@mod.route('/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required
def add_answer(question_id):
    """
    Function enables a logged in user to add an answer to a question on the
    platform.

    :params:
    question_id - holds the integer of the unique id of the question that the
    user wishes to answer.

    :returns:
    Question that was answered together with the answer for the question.

    An error message if the question does not exist.
    """
    data = request.get_json()

    answer = data.get('answer')

    user_id = get_jwt_identity()
    if not answer or answer.isspace():
        return jsonify({
            'message': 'Sorry, you did not enter any answer!'
        }), 400
    questions = Question.fetch_all_questions()
    if questions is None:
        return jsonify({
            'message': 'Sorry, there are no questions yet!'
        }), 400

    qn = Question.fetch_question_by_id(question_id)
    if qn is not None:
        db.insert_answer(user_id, question_id, answer)

        return jsonify({
            'Question': qn,
            'Answer': answer,
            'Message': 'Answer added succesfully!'
        }), 201
    return jsonify({
        'message': 'Sorry, this question does not exist!'
    }), 400


@mod.route('/questions/<int:question_id>', methods=['DELETE'])
@jwt_required
def delete_question(question_id):
    """
    Function enables a logged in user delete a question they created on the
    platform.

    :params:
    question_id - Holds the integer value of the unique id of the question that
    the user wishes to delete from the database.

    :returns:
    A success message when the question is succesfully deleted.

    An error message if the desired question does not exist.
    """
    user_id = get_jwt_identity()
    questions = Question.fetch_all_questions()
    if questions is None:
        return jsonify({
            'message': 'There are no questions to delete!'
        }), 400
    question = Question.fetch_one_question(user_id, question_id)
    answers = Answer.fetch_answers(question_id)
    if question:
        db.delete_question(user_id, question_id)
        if answers is not None or answers != []:
            db.delete_all_answers(question_id)
            return jsonify({
                'message': 'Question and answers deleted!'
            }), 200
        return jsonify({
            'message': 'Question deleted!'
        }), 200
    return jsonify({
        'message': 'Sorry, this question does not exist!'
    }), 400


@mod.route('/questions/<int:question_id>', methods=['PUT'])
@jwt_required
def modify_question(question_id):
    """
    Function enables a logged in user to modify the question they created on
    the platform.

    :params:
    question_id - Holds an integer value for the question that is going to be
    modified.

    :returns:
    The question which has been modified.

    An error message if the desired question does not exist.
    """
    data = request.get_json()

    question = data.get('question')

    user_id = get_jwt_identity()

    if not question or question.isspace():
        return jsonify({
            "message": "Sorry, you didn't enter any question!"
        }), 400
    question = Question.fetch_question_by_id(question_id)
    questions = Question.fetch_questions(user_id)
    if questions:
        if question:
            updated = Question.update_question(
                user_id, question_id, data['question']
            )
            return jsonify({
                "question": updated,
                "message": "Question updated successfully!"
            }), 201
        return jsonify({
            'message': 'Sorry, this question does not exist!'
        }), 400
    return jsonify({
        'message': 'Sorry, you have no questions to modify!'
    }), 400


@mod.route('/questions/<int:question_id>/answers/<int:answer_id>',
           methods=['PUT'])
@jwt_required
def accept_answer(question_id, answer_id):
    """
    Function enables a logged in question author mark the question as accepted.

    :params:
    question_id - Holds the integer value of the question whose answer is to be
    accepted.

    answer_id - Holds the integer value of the answer which is to be accepted.

    :returns:
    The question and accepted answer.

    An error message if either the question or answer does not exist.
    """
    user_id = get_jwt_identity()
    qn = Question.fetch_one_question(user_id, question_id)
    ans = Answer.fetch_answers(question_id)
    if qn:
        if not ans:
            return jsonify({
                'Answers': 'Sorry, this question has no answers yet!',
                'Question': qn,
                'message': 'Answers to this question were not found!'
            }), 400
        db.accept_answer(question_id, answer_id)
        accepted_answer = Answer.fetch_answers(question_id)
        return jsonify({
            'Answer': accepted_answer,
            'Question': qn,
            'message': 'Answer updated successfully!'
        }), 200
    else:
        return jsonify({
            'message': 'Sorry, that question does not exist!'
        }), 400


@mod.route('/question/<int:question_id>/answer/<int:answer_id>',
           methods=['PUT'])
@jwt_required
def modify_answer(question_id, answer_id):
    """
    Function enables a logged in user modify their answer to a question on the
    platform.

    :params:
    question_id - holds the integer value of the question id which is to be
    modified.

    answer_id - holds the integer value of the answer id which is to be
    modified.

    :returns:
    The modified answer incase of success.

    Appropriate error messages in case of failure.
    """
    data = request.get_json()

    answer = data.get('answer')

    user_id = get_jwt_identity()

    if not answer or answer.isspace():
        return jsonify({
            "message": "Sorry, you didn't enter any question!"
        }), 400
    qn = Question.fetch_question_by_id(question_id)
    ans = Answer.fetch_answers_by_user_id(user_id, question_id, answer_id)
    if not qn:
        return({
            'message': 'Sorry the question does not exist!'
        }), 400
    if not ans:
        return({
            'message': 'Sorry, this question does not have this answer yet!'
        }), 400
    db.update_answer(user_id, question_id, answer)
    return jsonify({
        'answer': ans,
        'message': 'Answer has been updated successfully!'
    })
