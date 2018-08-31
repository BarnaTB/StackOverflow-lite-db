# StackOverflow-lite

[![Build Status](https://travis-ci.org/BarnaTB/StackOverflow-lite-db.svg?branch=ft-api)](https://travis-ci.org/BarnaTB/StackOverflow-lite-db)

StackOverflow-lite is a platform where people can ask questions and provide answers.

## Getting Started

You can clone the project using the link [Github repository](https://github.com/BarnaTB/StackOverflow-lite.git).

## Prerequisites

The pages do not need much to be viewed as any web browser can view them from [this site](https://barnatb.github.io/StackOverflow-lite/) as long as they have internet access.

## Installing

* Clone the project into your local repository using this command:

`git clone https://github.com/BarnaTB/StackOverflow-lite-db.git`

* Change directory to the cloned folder using the following command for Windows, Linux and MacOS

`cd StackOverflow-lite-db`

* Switch to the ch-test-endpoints branch

`git checkout ch-test-endpoints`

* If you do not have a virtual environment installed run the following command, else follow the next steps.

`pip install virtualenv`

* Create a virtual environment(for Windows, Linux and MacOS)

`virtualenv venv`

* Activate the virtual environment(Windows only)

`source venv/Scripts/activate`

and for Linux and MacOS

`source venv/bin/activate`

* Install the app dependencies.(for Windows, Linux and MacOS)

`pip install -r requirements.txt`

* Run the app(for Windows, Linux and MacOS)

`python run.py`

* Copy the url http://127.0.0.1:5000/ into your Postman and to run any endpoint follow the table under the heading (**Endpoints**) with the url prefix ('/api/v1') for each endpoint.

## Running the tests

* If you don't have pytest installed, run the following command in your virtual environment:

`pip install pytest`

* Source the .env file using:

`source .env`

* Run the tests.

`py.test`

## Deployment

The UI pages are live on [github pages](https://barnatb.github.io/StackOverflow-lite/) and the python app is hosted on [heroku](https://stackoverflow-lite1.herokuapp.com/). They, however, have only been tested with Google Chrome and Mozilla Firefox so **no** assurance of perfomance in any other browser can be given.

## Endpoints

HTTP Method|Endpoint|Functionality|Parameters|Protected|
-----------|--------|-------------
POST|/signup|Register a user
POST|/login|Login a user
POST|/questions|Create a question
POST|/questions/int:questionId|Delete a question
GET|/questions/questionId|Fetch a specific question
GET|/questions|Fetch all questions
GET|/questions|Fetch all a specific user's questions
POST|/questions/questionId/answers|Add an answer
PUT|/questions/questionId/answers/answerId|Add an answer

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
