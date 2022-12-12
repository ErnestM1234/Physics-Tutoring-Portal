import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/tutor/student/dissolve')
def tutor_student_dissolve():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # this is temporary, this will be given to us by CAS or smth
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user['id']}, headers=headers)
    tutor = res.json()

    return render_template(
        '/tutor/tutor-student-dissolve.html',
        student=student,
        course=course,
        tutor=tutor, 
        user=user
    )