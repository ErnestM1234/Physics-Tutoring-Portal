import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/tutorships/create-tutorship/confirm', methods=['POST'])
def create_tutorship_confirm():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    student_id = request.form.get('student')
    tutor_id = request.form.get('tutor')
    course_id = request.form.get('course')
    status = 'ACCEPTED'

    if student_id is None or tutor_id is None or course_id is None or status is None:
        session['error_message'] = 'id field is missing'
        return redirect('/error/')


    # param validation
    if tutor_id.isnumeric() and int(float(tutor_id)) >= 0 and course_id.isnumeric() and int(float(course_id)) >= 0 and student_id.isnumeric() and int(float(student_id)) >= 0:
        validated_student_id = int(float(student_id))
        validated_tutor_id = int(float(tutor_id))
        validated_course_id = int(float(course_id))
    else:
        return redirect('/admin/create-tutor-course')

    data = {
        'tutor_id': validated_tutor_id,
        'course_id': validated_course_id,
        'student_id': validated_student_id,
        'status': status,
    }


    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    return redirect('/admin/tutorships/')

@app.route('/admin/tutorships/create-tutorship/')
def create_tutorship():

   # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')

     # get headers
    headers = get_header()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'is_tutor': True}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutors = res.json()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'is_student': True}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    students = res.json()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    courses = res.json()



    return render_template(
        '/admin/admin-create-tutorship.html',
        user=user, 
        tutors = tutors, 
        courses=courses, 
        students=students
    )

