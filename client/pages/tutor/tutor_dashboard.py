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
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()
    # redirect to application
    if user['is_tutor'] == False:
        return redirect('/tutor/tutorapplication')

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': user['id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'tutor_id': user['id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_courses = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'tutor_id': user['id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorships = res.json()


    for tutorship in tutorships:
        student_id = tutorship['student_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': student_id}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        student = res.json()
        tutorship['student'] = student

        course_id = tutorship['course_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        course = res.json()
        tutorship['course'] = course
   
    for tutor_course in tutor_courses:
        course_id = tutor_course['course_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        course = res.json()
        tutor_course['course'] = course

    
    accepted_tutorships = list(filter(lambda tutorship: tutorship['status'] == 'ACCEPTED', tutorships))
    requested_tutorships = list(filter(lambda tutorship: tutorship['status'] == 'REQUESTED', tutorships))

    accepted_tutor_courses = list(filter(lambda tutor_course: tutor_course['status'] == 'ACCEPTED', tutor_courses))

    other_tutor_courses = list(filter(lambda tutor_course: tutor_course['status'] != 'ACCEPTED', tutor_courses))

    return render_template(
        '/tutor/tutor-dashboard.html', tutor=tutor, accepted_tutorships=accepted_tutorships, requested_tutorships=requested_tutorships, accepted_tutor_courses=accepted_tutor_courses, other_tutor_courses=other_tutor_courses, tutor_courses = tutor_courses, user=user
    )