import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/tutor/request/confirm')
def student_tutor_request_confirm():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            'student-no-access.html',
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

    requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps({'tutor_id': tutor_id, 'course_id': course_id, 'student_id': user['id'], 'status': 'REQUESTED'}), headers=headers)

    return render_template(
        'student-tutor-request-confirm.html',
        user=user,
        course=course,
        tutor=tutor
    )
