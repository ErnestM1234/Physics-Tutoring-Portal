# run the following command to start the server: $ gunicorn app:app

from os import environ as env
from flask import Flask, render_template, redirect, session, url_for
import requests
from dotenv import find_dotenv, load_dotenv
import auth.auth as auth
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
import http.client

# env
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# app
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# setup OAuth
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# OAuth Routes
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user_info = token["userinfo"]

    # check if this user already exists
    res = requests.post(
        url = str(os.environ['API_ADDRESS']+'/api/user-auth-id/'),
        headers={"authorization": "Bearer " + token["id_token"]},
        data=json.dumps({"auth_id": user_info["sub"]})
    )
    user = res.json()
    # log out when failure connecting to backend 
    if res.status_code != 200:
        session.clear()

    # check if user exists
    if 'id' not in user.keys():
        # create new user when user not found
        data = {
            "netid": user_info["nickname"],
            "name" : user_info["name"],
            "email": user_info["email"],
        }
        res = requests.post(
            url = str(os.environ['API_ADDRESS']+'/api/user/create/'),
            headers={"authorization": "Bearer " + token["id_token"]},
            data=json.dumps(data)
        )
        # log out when failure creating new user
        if res.status_code != 200:
            print('failed to create new user')
            session.clear()
    
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/dashboard')
def dashboard():

    student_tutorships = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={"id": 1})
    student_tutorships = student_tutorships.json()

    tutors = []

    for tutorship in student_tutorships:
        tutor_id = tutorship["tutor_id"]
        student_tutors = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={"id": tutor_id})
        student_tutors = student_tutors.json()
        tutors.append(student_tutors)

    print("-------------------")
    print(tutors)

    return render_template(
        'dashboard.html',
        tutors = tutors
    )








@app.route('/tutordashboard')
def tutor_dashboard():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    tutor_id = 1
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_id})
    tutor = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'tutor_id': tutor_id})
    tutor_courses = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'tutor_id': tutor_id})
    tutorships = res.json()

    for tutorship in tutorships:
        student_id = tutorship['student_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': student_id})
        student = res.json()
        tutorship['student'] = student

        course_id = tutorship['course_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id})
        course = res.json()
        tutorship['course'] = course
   
    for tutor_course in tutor_courses:
        course_id = tutor_course['course_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id})
        course = res.json()
        tutor_course['course'] = course


    return render_template(
        'tutordash.html', tutor=tutor, tutorships=tutorships, tutor_courses=tutor_courses
    )

@app.route('/allclasses')
def allClasses():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))
    courses = res.json()
   
    return render_template(
        'allclasses.html', courses=courses
    )

@app.route('/editbio')
def editBio():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    tutor_id = 1
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_id})
    tutor = res.json()

    return render_template(
        'editbio.html', tutor=tutor
    )



@app.route('/editbio/confirm', methods=['POST'])
def edit_bio_confirm():

    bio = request.form.get('bio')
    tutor_id = request.form.get('tutor_id')

    if bio is None or tutor_id is None:
        return redirect('/editbio')

   
    data = {
        'bio': bio,
        'id': tutor_id
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps(data))
   
    message = str(res)


    return render_template(
        'confirmationtutor.html',
        message=message
    )


# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
# pylint: disable-next=unused-wildcard-import
# pylint: disable-next=wildcard-import
from pages.admin_dashboard import *
from pages.admin_courses import *
from pages.admin_tutorships import *
from pages.admin_tutors import *
from pages.admin_students import *
from pages.admin_admins import *
from pages.create_course import *
from pages.create_tutor_course import *
from pages.create_tutorship import *
from pages.create_user import *
from pages.remove_course import *
from pages.remove_tutorship import *
from pages.student_profile import *
from pages.tutor_profile import *


from pages.student_dashboard import *
from pages.student_courses import *
from pages.student_course import *
from pages.student_tutor import *
from pages.student_tutor_request import *
from pages.student_tutor_cancel import *
from pages.student_tutor_dissolve import *
from pages.student_tutor_request_confirm import *
from pages.student_tutor_cancel_confirm import *
from pages.student_tutor_dissolve_confirm import *


if __name__ == '__main__':
    app.run()