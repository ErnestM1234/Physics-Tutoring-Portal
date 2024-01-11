import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()


@app.route('/admin/course/')
def admin_course():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')

    # get headers
    headers = get_header()

    # param validation
    course_id = request.args.get('course_id')
    params = {"course_id": None}
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            params['course_id'] = int(float(course_id))
            course_id = int(float(course_id))
        else:
            session['error_message'] = "You have supplied an incorrect course id"
            return redirect('/error/')
    
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    course = res.json()

    # get tutorships (deep)
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/deep/'), params=params, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorships = res.json()

    # get tutor_courses (deep)
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/deep/'), params=params, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_courses = res.json()

    # list of approved tutors
    approved_tutor_courses = list(filter(lambda tutor_course: tutor_course['status'] in ('ACCEPTED', 'UNAVAILABLE'), tutor_courses))

    # list of requested tutor_courses
    tutor_course_requests = list(filter(lambda tutor_course: tutor_course['status'] == 'REQUESTED', tutor_courses))


  
    return render_template(
        '/admin/admin-course.html',
        user=user,
        tutorships=tutorships,
        course=course,
        course_id=course_id,
        approved_tutor_courses=approved_tutor_courses,
        tutor_course_requests=tutor_course_requests,
    )


