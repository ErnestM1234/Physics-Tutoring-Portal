
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/tutor/student')
def tutor_student():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    student_id = request.args.get('student_id')
    course_id = request.args.get('course_id')

    print(student_id, course_id)

    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': student_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    student = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    course = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id, 'tutor_id': user['id'], 'course_id': course_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorship = res.json()

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]

    return render_template(
        '/tutor/tutor-student.html',
        user=user,
        student=student,
        course=course,
        tutorship = tutorship
    )
