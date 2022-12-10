
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
    
    # get headers
    headers = get_header()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'id': 1}, headers=headers)
    user = res.json()

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
        '/student/student-dashboard.html',
        user=user,
        tutorships=tutorships
    )
