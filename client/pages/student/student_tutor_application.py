import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/tutor/application')
def studentTutorApplication():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            '/student/student-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    course_id = request.args.get('course_id')
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
    course = res.json()

    return render_template(
        '/student/student-tutor-application.html', course = course, user=user
    )