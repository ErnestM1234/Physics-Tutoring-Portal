
import os
from dotenv import load_dotenv
from app import app
import time
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/courses')
def student_courses():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            '/student/student-no-access.html',
            message='you do not have permission to access this page'
        )
    
    # get headers
    headers = get_header()

    # get courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    courses = res.json()

    # Get current time in GMT
    now = time.struct_time(time.gmtime())

    # Get year
    semester = str(now[0])

    # Divide into spring/fall semester
    if now[1] < 7:
        semester = "Spring " + semester
    else:
        semester = "Fall " + semester

    return render_template(
        '/student/student-courses.html',
        user=user,
        courses=courses,
        semester=semester
    )
