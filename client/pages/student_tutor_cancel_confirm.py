import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/tutor/cancel/confirm')
def student_tutor_cancel_confirm():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

     # TO CHANGE
    course_id = request.args.get('course_id')
    tutor_id = request.args.get('tutor_id')

     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": tutor_id}, headers=headers)
    tutor = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': user['id'], 'tutor_id': tutor_id, 'course_id': course_id}, headers=headers)
    tutorship = res.json()

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/delete/'), data=json.dumps({'id': tutorship['id']}))

    return render_template(
        'student-tutor-cancel-confirm.html',
        user=user,
        course=course,
        tutor=tutor
    )
