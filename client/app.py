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
from pages.shared.get_user import *

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
    if session is None or session.get('user') is None:
        return render_template("landing.html")
    return redirect("/student/dashboard")





















































# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
# pylint: disable-next=unused-wildcard-import
# pylint: disable-next=wildcard-import
from pages.admin.admin_dashboard import *
from pages.admin.admin_courses import *
from pages.admin.admin_tutorships import *
from pages.admin.admin_tutors import *
from pages.admin.admin_students import *
from pages.admin.admin_admins import *
from pages.admin.admin_create_course import *
from pages.admin.admin_create_tutor_course import *
from pages.admin.admin_create_tutorship import *
from pages.admin.admin_create_user import *
from pages.admin.admin_remove_course import *
from pages.admin.admin_remove_tutorship import *
from pages.admin.admin_student_profile import *
from pages.admin.admin_tutor_profile import *
from pages.admin.admin_add_admin import *


from pages.student.student_dashboard import *
from pages.student.student_courses import *
from pages.student.student_course import *
from pages.student.student_tutor import *
from pages.student.student_tutor_request import *
from pages.student.student_tutor_cancel import *
from pages.student.student_tutor_dissolve import *
from pages.student.student_tutor_request_confirm import *
from pages.student.student_tutor_cancel_confirm import *
from pages.student.student_tutor_dissolve_confirm import *
from pages.student.student_tutor_application import *
from pages.student.student_tutor_courses import *
from pages.student.student_application_confirm import *

from pages.tutor.tutor_dashboard import*
from pages.tutor.tutor_courses import*
from pages.tutor.tutor_application import*
from pages.tutor.tutor_application_confirm import*
from pages.tutor.tutor_editbio import*
from pages.tutor.tutor_editbio_confirm import*
from pages.tutor.tutor_student_accept_confirm import*
from pages.tutor.tutor_student_accept import*
from pages.tutor.tutor_student_dissolve_confirm import*
from pages.tutor.tutor_student_dissolve import*
from pages.tutor.tutor_student_reject_confirm import *
from pages.tutor.tutor_student_reject import *



if __name__ == '__main__':
    app.run()