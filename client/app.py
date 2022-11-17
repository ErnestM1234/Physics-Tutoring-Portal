# run the following command to start the server: $ gunicorn app:app

import os
<<<<<<< HEAD
import flask 
from flask import Flask, render_template
=======
from flask import Flask, render_template, redirect
>>>>>>> 335dfe2f83cc00728266079562b32ad2f228bacb
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

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'is_student': True})
    students = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    data = res.json()

    names=[]
    netids=[]
    emails=[]

    for user in data:
        names.append(user['name'])
        netids.append(user['netid'])
        emails.append(user['email'])

    data = zip(names, netids, emails)
    return render_template(
<<<<<<< HEAD
        'tutordash.html', data = data
    )

@app.route('/allclasses')
def allClasses():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    
    return render_template(
        'allclasses.html'
    )

@app.route('/editbio')
def editBio():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    tutorbio = flask.request.args.get('tutorbio')

    return render_template(
        'editbio.html', tutorbio=tutorbio
    )
=======
        'tutordash.html'
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
from pages.student_profile import *
from pages.tutor_profile import *


if __name__ == '__main__':
    app.run()
>>>>>>> 335dfe2f83cc00728266079562b32ad2f228bacb
