# StackOverflow-lite

[![Build Status](https://travis-ci.org/BarnaTB/StackOverflow-lite-db.svg?branch=ft-api)](https://travis-ci.org/BarnaTB/StackOverflow-lite-db)

StackOverflow-lite is a platform where people can ask questions and provide answers.

## Getting Started

You can clone the project using the link [Github repository](https://github.com/BarnaTB/StackOverflow-lite.git).

## Prerequisites

The pages do not need much to be viewed as any web browser can view them from [this site](https://barnatb.github.io/StackOverflow-lite/) as long as they have internet access.

## Installing

* Clone the project into your local repository using this command:

```sh
  $ git clone https://github.com/BarnaTB/StackOverflow-lite-db.git
  ```
  Switch to the cloned directory, install a virtual environment, create a virtual environment, activate it, install app dependencies and run the app.
  ```sh
    $ cd StackOverflow-lite-db
    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python run.py
```
**Note** If you're using Windows, activate your virtualenv using `` $ source venv/Scripts/activate ``
* Copy the url http://127.0.0.1:5000/ into your Postman and to run any endpoint follow the table under the heading (**Endpoints**) with the url prefix ('/api/v1') for each endpoint.

## Endpoints
HTTP Method | Endpoint | Functionality | Parameters | Protected
----------- | -------- | ------------- | ---------- | ---------
POST | /signup | Register a user| None | False
POST | /login | Login a user | None | False
POST | /questions | Create a question | None | True
POST | /questions/int:question_id | Delete a question | question_id | True
GET | /questions/questionId | Fetch a specific question | question_id | True
GET | /questions | Fetch all questions | None | True
GET | /questions | Fetch all a specific user's questions | None | True
POST | /questions/questionId/answers | Add an answer | question_id | True
PUT | /questions/questionId/answers/answerId | Add an answer | question_id, answer_id | True

## Running the tests

Install pytest, source the .env file, run the tests.
```sh
  $ pip install pytest
  $ source .env
  $ pytest
  ```

## Deployment

The UI pages are live on [github pages](https://barnatb.github.io/StackOverflow-lite/) and the python app is hosted on [heroku](https://stackoverflow-lite1.herokuapp.com/). They, however, have only been tested with Google Chrome and Mozilla Firefox so **no** assurance of perfomance in any other browser can be given.

## Tools Used

* [Flask](http://flask.pocoo.org/) - Web microframework for Python
* [Virtual environment](https://virtualenv.pypa.io/en/stable/) - tool used to create isolated python environments
* [pip](https://pip.pypa.io/en/stable/) - package installer for Python

## Built With

The project has been built with the following technologies so far:

* HTML
* CSS
* Javascript
* Python/Flask
* PostgreSQL

## Contributions

To contibute to the project, create a branch from the *develop* branch and make a PR after which your contributions may be merged into the **develop** branch

## Authors

Barnabas Tumuhairwe B

## Acknowledgements

Kudos to the developers at Andela for their unmatched support during the development of this project.
