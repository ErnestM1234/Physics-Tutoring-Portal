
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/course')
def student_course():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            '/student/student-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    # TO CHANGE
    course_id = request.args.get('id')

    # get approved tutors
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'course_id': course_id, 'status': 'ACCEPTED'}, headers=headers)
    tutor_courses = res.json()

    for tutor_course in tutor_courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_course['tutor_id']}, headers=headers)
        tutor = res.json()
        tutor_course['tutor'] = tutor

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
    course = res.json()

    return render_template(
        '/student/student-course.html',
        user=user,
        tutor_courses=tutor_courses,
        course=course
    )
