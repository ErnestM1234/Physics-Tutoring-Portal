# run the following command to start the server: $ gunicorn app:app

import datetime
from os import environ as env
from flask import Flask, render_template, redirect, session
import requests
from dotenv import find_dotenv, load_dotenv
import auth.auth as auth
import json
from pages.shared.get_user import *
from services.oit import *


# env
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# app
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")



@app.route("/")
def home():
    return render_template('landing.html')


# Routes for authentication.

@app.route('/login', methods=['GET'])
def login():
    netid = auth.authenticate()
    encoded_jwt = jwt.encode({
            "netid": netid,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }, os.environ['APP_SECRET_KEY'], algorithm="HS256")

    # get credential level
    user = get_user(requests)
    res = requests.post(
        url = str(os.environ['API_ADDRESS']+'/api/user-auth-id/'),
        headers={"authorization": encoded_jwt},
        data=json.dumps({"netid": netid})
    )
    user = res.json()
    # log out when failure connecting to backend 
    if res.status_code != 200:
        print('failed to get user')
        session.clear()
        return 'failed login'



    # check if user exists
    if 'id' not in user.keys():
        # get user info
        user_info = get_basic_student(netid)


        # create new user when user not found
        data = {
            "netid": netid,
            "name" : user_info["name"],
            "email": user_info["mail"],
        }
        res = requests.post(
            url = str(os.environ['API_ADDRESS']+'/api/user/create/'),
            headers={"authorization": encoded_jwt},
            data=json.dumps(data)
        )
        # log out when failure creating new user
        if res.status_code != 200:
            print('failed to create new user')
            session.clear()
        
            return 'failed login'
        print('created new user, directing to student dashboard')
        return redirect('/student/dashboard')
    else:
        # route them to correct page
        if user['is_admin'] == True:
            return redirect('/admin/dashboard')
        if user['is_tutor'] == True:
            return redirect('/tutor/dashboard')
        if user['is_student'] == True:
            return redirect('/student/dashboard')
    
        return 'Something went wrong! You are not a student!'

@app.route('/logout', methods=['GET'])
def logout():
    return redirect('/logoutcas')

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

















































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
from pages.student.student_tutors_request import *
from pages.student.student_tutors_request_confirm import *

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

from pages.error.error_page import *



if __name__ == '__main__':
    app.run()