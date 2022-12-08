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








@app.route('/tutor/dashboard')
def tutor_dashboard():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys():
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()
    # redirect to application
    if user['is_tutor'] == False:
        return redirect('/tutorapplication')

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': user['id']}, headers=headers)
    tutor = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'tutor_id': user['id']}, headers=headers)
    tutor_courses = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'tutor_id': user['id']}, headers=headers)
    tutorships = res.json()


    for tutorship in tutorships:
        student_id = tutorship['student_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': student_id}, headers=headers)
        student = res.json()
        tutorship['student'] = student

        course_id = tutorship['course_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
        course = res.json()
        tutorship['course'] = course
   
    for tutor_course in tutor_courses:
        course_id = tutor_course['course_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
        course = res.json()
        tutor_course['course'] = course

    
    accepted_tutorships = list(filter(lambda tutorship: tutorship['status'] == 'ACCEPTED', tutorships))
    requested_tutorships = list(filter(lambda tutorship: tutorship['status'] == 'REQUESTED', tutorships))



    return render_template(
        'tutor-dashboard.html', tutor=tutor, accepted_tutorships=accepted_tutorships, requested_tutorships=requested_tutorships, tutor_courses = tutor_courses
    )

@app.route('/tutor/courses')
def allClasses():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'), headers=headers)
    courses = res.json()
   
    return render_template(
        'tutor-courses.html', courses=courses
    )

@app.route('/tutor/editbio')
def editBio():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': user['id']}, headers=headers)
    tutor = res.json()

    return render_template(
        'tutor-editbio.html', tutor=tutor
    )

@app.route('/tutor/application')
def tutorApplication():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'), headers=headers)
    courses = res.json()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': user['id']}, headers=headers)
    tutor = res.json()

    return render_template(
        'tutor-application.html', courses=courses, tutor=tutor
    )



@app.route('/tutor/editbio/confirm', methods=['POST'])
def edit_bio_confirm():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    bio = request.form.get('bio')

    if bio is None:
        return redirect('/editbio')

   
    data = {
        'bio': bio,
        'id': user['id']
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps(data), headers=headers)
   
    message = str(res)


    return render_template(
        'confirmationtutor.html',
        message=message
    )



@app.route('/tutor/application/confirm', methods=['POST'])
def tutor_application_confirm():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    course_id = request.form.get('course_id')
    taken_course = request.form.get('taken_course')
    experience = request.form.get('experience')

   
    data = {
        'tutor_id': user['id'],
        'course_id': course_id,
        'taken_course': taken_course,
        'experience': experience,
        'status': 'REQUESTED'
    }

    # mark student as a tutor
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps({'id': str(user['id']), 'is_tutor': True}), headers=headers)
    if res.status_code != 200:
        return render_template(
            'confirmationtutor.html',
            message='Error: '  + str(res.content)
        )

    # create relationship btwn tutor and course
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/create/'), data=json.dumps(data), headers=headers)
    message = str(res)
    if res.status_code != 200:
        return render_template(
            'confirmationtutor.html',
            message='Error: ' + str(res.content)
        )


    return render_template(
        'confirmationtutor.html',
        message=message
    )


@app.route('/tutor/student/dissolve')
def tutor_student_dissolve():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # this is temporary, this will be given to us by CAS or smth
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user['id']}, headers=headers)
    tutor = res.json()

    return render_template(
        'tutor-student-dissolve.html',
        student=student,
        course=course,
        tutor=tutor
    )

@app.route('/tutor/student/dissolve/confirm')
def tutor_student_dissolve_confirm():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


     # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()


     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user['id']}, headers=headers)
    tutor = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id, 'tutor_id': user['id'], 'course_id': course_id}, headers=headers)
    tutorship = res.json()
    
    print("len")
    print(len(tutorship))
    print("tutorship")
    print(tutorship)

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/delete/'), data=json.dumps({'id': tutorship['id']}), headers=headers)

    return render_template(
        'tutor-student-dissolve-confirm.html',
        student=student,
        course=course,
        tutor=tutor
    )


@app.route('/tutor/student/accept')
def tutor_student_accept():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user['id']}, headers=headers)
    tutor = res.json()

    return render_template(
        'tutor-student-accept.html',
        student=student,
        course=course,
        tutor=tutor
    )

@app.route('/tutor/student/accept/confirm')
def tutor_student_accept_confirm():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


     # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()


     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user['id']}, headers=headers)
    tutor = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id, 'tutor_id': user['id'], 'course_id': course_id}, headers=headers)
    tutorship = res.json()
    

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/update'), data=json.dumps({'id': tutorship['id'], 'status': 'ACCEPTED'}), headers=headers)

    return render_template(
        'tutor-student-accept-confirm.html',
        student=student,
        course=course,
        tutor=tutor
    )



@app.route('/tutor/student/reject')
def tutor_student_reject():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user['id']}, headers=headers)
    tutor = res.json()

    return render_template(
        'tutor-student-reject.html',
        student=student,
        course=course,
        tutor=tutor
    )

@app.route('/tutor/student/reject/confirm')
def tutor_student_reject_confirm():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


     # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()


     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user['id']}, headers=headers)
    tutor = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id, 'tutor_id': user['id'], 'course_id': course_id}, headers=headers)
    tutorship = res.json()
    

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/update'), data=json.dumps({'id': tutorship['id'], 'status': 'REJECTED'}), headers=headers)

    return render_template(
        'tutor-student-reject-confirm.html',
        student=student,
        course=course,
        tutor=tutor
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