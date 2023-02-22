# run the following command to start the server: $ gunicorn app:app

import datetime
from os import environ as env
from flask import Flask, render_template, redirect, send_from_directory, session, url_for
import requests
from dotenv import find_dotenv, load_dotenv
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


# favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')




























# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
# pylint: disable-next=unused-wildcard-import
# pylint: disable-next=wildcard-import
from auth.auth import *

from pages.admin.admin_dashboard import *
from pages.admin.admin_courses import *
from pages.admin.admin_tutorships import *
from pages.admin.admin_tutors import *
from pages.admin.admin_update_tutor_course import *
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
from pages.admin.admin_remove_admin import *
from pages.admin.admin_course import *
from pages.admin.admin_tutorship import *
from pages.admin.admin_tutor_course import *


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
from pages.tutor.tutor_edit_profile import*
from pages.tutor.tutor_edit_profile_confirm import*
from pages.tutor.tutor_student_accept_confirm import*
from pages.tutor.tutor_student_accept import*
from pages.tutor.tutor_student_dissolve_confirm import*
from pages.tutor.tutor_student_dissolve import*
from pages.tutor.tutor_student_reject_confirm import *
from pages.tutor.tutor_student_reject import *
from pages.tutor.tutor_student import *

from pages.error.error_page import *



if __name__ == '__main__':
    app.run()