import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()


@app.route('/tutor/dashboard')
def tutor_dashboard():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys():
        return render_template(
            'tutor-no-access.html',
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