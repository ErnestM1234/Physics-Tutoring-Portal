
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/dashboard')
def student_dashboard():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            '/student/student-no-access.html',
            message='you do not have permission to access this page'
        )
    
    # get headers
    headers = get_header()

    # get tutorships, tutors, and courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/deep/'), params={'student_id': user['id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorships = res.json()

    # get tutor courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/deep/'), params={'tutor_id': user['id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_courses = res.json()

    return render_template(
        '/student/student-dashboard.html',
        user=user,
        tutorships=tutorships,
        tutor_courses=tutor_courses
    )
