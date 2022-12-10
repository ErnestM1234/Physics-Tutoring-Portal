# run the following command to start the server: $ gunicorn app:app

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_oauth2 import ResourceProtector
from src.utils.validator import Auth0JWTBearerTokenValidator, decode
from authlib.integrations.flask_client import OAuth

load_dotenv()


# Authentication
require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    str(os.environ['AUTH0_DOMAIN']),
    str(os.environ['AUTH0_AUDIENCE'])
)
require_auth.register_token_validator(validator)

# start server
app = Flask(__name__)

# # select what server to run (local, dev, prod) based on env
app.config.from_object(os.environ['APP_SETTINGS'])

# reference to database
db = SQLAlchemy(app)

# context
context = { 'auth_id': None }

# (clear db and ) put all tables into db
# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
from src.database.models import *
with app.app_context():
    #db.drop_all() # this is temporary fix for running db migrations (remove this line in future)
    db.create_all()


# @app.route("/api/print-token")
# def print_token():
#     token = request.args['token']
#     decode(token)
#     return 'hi'

# # Authentication Routes
# @app.route("/api/public")
# def public():
#     """No access token required."""
#     response = (
#         "Hello from a public endpoint! You don't need to be"
#         " authenticated to see this."
#     )
#     return jsonify(message=response)


# @app.route("/api/private")
# @require_auth(None)
# def private():
#     """A valid access token is required."""
#     response = (
#         "Hello from a private endpoint! You need to be"
#         " authenticated to see this."
#     )
#     return jsonify(message=response)


# @app.route("/api/private-scoped")
# @require_auth("read:messages")
# def private_scoped():
#     """A valid access token and scope are required."""
#     response = (
#         "Hello from a private endpoint! You need to be"
#         " authenticated and have a scope of read:messages to see"
#         " this."
#     )
#     return jsonify(message=response)

# @app.route('/')
# def hello_world():
#     return 'Physics Tutoring Portal Client Time!'


# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
# pylint: disable-next=unused-wildcard-import
# pylint: disable-next=wildcard-import
from src.api.user.user import *
from src.api.course.course import *
from src.api.tutorship.tutorship import *
from src.api.tutor_course.tutor_course import *


if __name__ == '__main__':
    app.run()
