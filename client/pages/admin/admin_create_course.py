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
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    name = request.form.get('name')
    dept_course = request.form.get('dept_course')

    if name is None or name == "" or dept_course is None or dept_course == "":
        session['error_message'] = 'Name or Dept_Course field is missing a value'
        return redirect('/error/')

    
    data = {
        'name': name,
        'dept_course': dept_course
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/course/create/'), data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    
    message = str(res)

    return render_template(
        '/admin/confirmation.html',
        message=message
    )

@app.route('/admin/courses/create-course')
def create_course():

    # verify is admin
    user = get_user(requests)
    if "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        


    return render_template(
        '/admin/admin-create-course.html',
    )

