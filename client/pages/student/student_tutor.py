
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/tutor')
def student_tutor():
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
    tutor_id = request.args.get('tutor_id')
    course_id = request.args.get('course_id')

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_id}, headers=headers)
    tutor = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
    course = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': user['id'], 'tutor_id': tutor_id, 'course_id': course_id}, headers=headers)
    tutorship = res.json()

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]

    return render_template(
        '/student/student-tutor.html',
        user=user,
        tutor=tutor,
        course=course,
        tutorship = tutorship
    )
