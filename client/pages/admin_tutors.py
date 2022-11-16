import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template

load_dotenv()

@app.route('/admin/tutors')
def admin_tutors():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'))
    tutor_courses = res.json()

    approved_tutor_courses = list(filter(lambda tutor_course: tutor_course['status'] != 'REQUESTED', tutor_courses))


    student_count = []
    # todo: make a specific endpoint for this
    for tutor_course in tutor_courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={"tutor_id": tutor_course['tutor_id']})
        tutorships = res.json()
        student_count.append(len(tutorships))

    tutor_requests = list(filter(lambda tutor_course: tutor_course['status'] == 'REQUESTED', tutor_courses))


    return render_template(
        'admin-tutors.html',
        tutor_courses=approved_tutor_courses,
        student_count=student_count,
        tutor_requests=tutor_requests
    )

