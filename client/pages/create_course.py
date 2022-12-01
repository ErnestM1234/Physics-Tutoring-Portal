import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/courses/create-course/confirm', methods=['POST'])
def create_course_confirm():

    # verify is admin
    user = get_user(requests)
    if "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    name = request.form.get('name')
    dept_course = request.form.get('dept_course')

    if name is None or dept_course is None:
        return redirect('/')

    
    data = {
        'name': name,
        'dept_course': dept_course
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/course/create/'), data=json.dumps(data), headers=headers)
    
    message = str(res)


    return render_template(
        'confirmation.html',
        message=message
    )

@app.route('/admin/courses/create-course')
def create_course():

    # verify is admin
    user = get_user(requests)
    if "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )


    return render_template(
        'create-course.html',
    )

