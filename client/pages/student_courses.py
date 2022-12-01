
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/courses')
def student_courses():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    # get courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'), headers=headers)
    courses = res.json()

    return render_template(
        'student-courses.html',
        user=user,
        courses=courses
    )
