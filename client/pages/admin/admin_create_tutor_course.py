import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/create-tutor-course/confirm', methods=['POST'])
def create_tutor_course_confirm():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    tutor_id = request.form.get('tutor')
    course_id = request.form.get('course')
    status = request.form.get('status')

    print(tutor_id)
    print(course_id)
    print(status)

    if tutor_id is None or course_id is None or status is None:
        return redirect('/admin/create-tutor-course')


    # param validation
    if tutor_id.isnumeric() and int(float(tutor_id)) >= 0 and course_id.isnumeric() and int(float(course_id)) >= 0:
        validated_tutor_id = int(float(tutor_id))
        validated_course_id = int(float(course_id))
    else:
        return redirect('/admin/create-tutor-course')

    data = {
        'tutor_id': validated_tutor_id,
        'course_id': validated_course_id,
        'status': status,
    }



    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/create'), data=json.dumps(data), headers=headers)
    
    message = str(res)
    print(res.content)


    return render_template(
        '/admin/confirmation.html',
        message=message
    )

@app.route('/admin/create-tutor-course')
def create_tutor_course():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    
    # get headers
    headers = get_header()


    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'is_tutor': True}, headers=headers)
    tutors = res.json()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'), headers=headers)
    courses = res.json()


    return render_template(
        '/admin/admin-create-tutor-course.html', 
        tutors = tutors, 
        courses=courses
    )

