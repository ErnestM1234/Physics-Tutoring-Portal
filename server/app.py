# run the following command to start the server: $ gunicorn app:app

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()

# start server
app = Flask(__name__)


# select what server to run (local, dev, prod) based on env
app.config.from_object(os.environ['APP_SETTINGS'])

# reference to database
db = SQLAlchemy(app)

# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
from models import Users
with app.app_context():
    db.drop_all() # this is temporary fix for running db migrations
    db.create_all()

@app.route('/')
def hello_world():
    return 'Physics Tutoring Portal Client Time!'


if __name__ == '__main__':
    app.run()
