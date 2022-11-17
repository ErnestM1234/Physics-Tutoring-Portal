# run the following command to start the server: $ gunicorn app:app

import os
import flask
from flask import Flask, render_template, redirect
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    # todo: should this autoroute to one of the three dashboards??

    # request list of users
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    res2 = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'))
    res3 = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))

    data = res.json()
    data2 = res2.json()
    data3 = res3.json()
    # return 'hi'
    return render_template(
        'users.html',
        users=data,
        tutorships=data2,
        courses=data3
    )

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


if __name__ == '__main__':
    app.run()


