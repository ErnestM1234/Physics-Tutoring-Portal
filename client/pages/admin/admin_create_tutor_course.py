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

    tutor_id = request.form.get('tutor_id')
    course_id = request.form.get('course_id')
    status = request.form.get('status')

    if tutor_id is None or course_id is None or status is None:
        return redirect('/')


    # param validation
    if tutor_id.isnumeric() and int(float(tutor_id)) >= 0 and course_id.isnumeric() and int(float(course_id)) >= 0:
        validated_tutor_id = int(float(tutor_id))
        validated_course_id = int(float(course_id))
    else:
        return redirect('/')

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


    return render_template(
        '/admin/admin-create-tutor-course.html',
    )

