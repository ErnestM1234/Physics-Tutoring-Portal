# run the following command to start the server: $ gunicorn app:app

import os
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
    return render_template(
        'tutordash.html'
    )

@app.route('/admindashboard')
def admin_dashboard():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    print(user)
    # verify is admin
    if id not in user.keys() or user['is_admin'] == False:
        return redirect('/')

    # get courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))
    courses = res.json()

    # get tutors by coures
    # get tutees by course


    # todo(Ernest): spin up a diff process for these requests?? these two is a bit ~C~ ~H~ ~U~ ~N~ ~K~ ~Y~
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'status': "APPROVED"})
    tutors = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'status': "APPROVED"})
    tutorships = res.json()

    approved_tutors_count = []
    available_tutors_count = []
    tutees_count = []
    for course in courses: # todo (Ernest): this runs in like O(N^2) time. It can run in O(N) time. ATM I am too lazy to optimize this
        filtered_tutors = tutors

        # calculate approved tutors
        approved_tutors_count.append(len(list(filter(lambda tutor: tutor['course_id'] == course['id'], tutors))))

        # calculate available tutors
        available_tutors_count.append(3) # todo (Ernest): requires updates to the schema

        # calculate active tutees
        tutees_count.append(len(list(filter(lambda tutorships: tutorships['course_id'] == tutorships['id'], tutorships))))




    return render_template(
        'admindashboard.html',
        user=user,
        courses=courses,
        approved_tutors_count=approved_tutors_count,
        available_tutors_count=available_tutors_count,
        tutees_count=tutees_count
    )

