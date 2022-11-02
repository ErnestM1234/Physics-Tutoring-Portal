import os
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from .env
load_dotenv()

# Create SQLAlchemy engine based on environment variable
engine = create_engine(os.environ['DATABASE_URL'])

# Start server
app = flask.Flask(__name__, template_folder='.')

# Select which server to run (local, dev, prod) based on environment variable
app.config.from_object(os.environ['APP_SETTINGS'])

# Reference to the database
db = SQLAlchemy(app)

# Import necessary classes; update as needed
from models import Classes

# Delete existing tables in the database and create empty ones
with app.app_context():
    db.drop_all() # this is temporary fix for running db migrations
    db.create_all()

# Homepage
@app.route('/')
def hello_world():
    return 'Physics Tutoring Portal Client Time!'

# Page for adding classes
@app.route('/add-class')
def add_class():
    # Get user's input from class creation form
    number = flask.request.args.get('number')
    title = flask.request.args.get('title')

    if number is None:
        number = ''

    if title is None:
        title = ''

    # Create an SQL statement for inserting a new class
    stmt = db.insert(Classes).values(name = title, dept_course = number)

    # Use the SQLAlchemy engine to insert a new class into the database
    with engine.connect() as conn:
        result = conn.execute(stmt)

    # Get all courses
    courses = Classes.query.all()

    html_code = flask.render_template('add-class.html', courses = courses, number = number, title = title)
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run()
