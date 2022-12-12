# run the following command to start the server: $ gunicorn app:app

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

# start server
app = Flask(__name__)

# # select what server to run (local, dev, prod) based on env
app.config.from_object(os.environ['APP_SETTINGS'])

# reference to database
db = SQLAlchemy(app)

# context
context = { 'netid': None }

# (clear db and ) put all tables into db
# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
from src.database.models import *
with app.app_context():
    db.drop_all() # this is temporary fix for running db migrations (remove this line in future)
    db.create_all()


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
