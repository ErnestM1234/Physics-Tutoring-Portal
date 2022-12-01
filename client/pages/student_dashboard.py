
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/dashboard')
def student_dashboard():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': user['id']}, headers=headers)
    tutorships = res.json()

    for tutorship in tutorships:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship['tutor_id']}, headers=headers)
        tutor = res.json()
        tutorship['tutor'] = tutor

        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship['course_id']}, headers=headers)
        course = res.json()
        tutorship['course'] = course

    return render_template(
        'student-dashboard.html',
        user=user,
        tutorships=tutorships
    )
