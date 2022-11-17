import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/courses/create-course/confirm', methods=['POST'])
def create_course_confirm():

    name = request.form.get('name')
    dept_course = request.form.get('dept_course')

    if name is None or dept_course is None:
        return redirect('/')

    
    data = {
        'name': name,
        'dept_course': dept_course
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/course/create/'), data=json.dumps(data))
    
    message = str(res)


    return render_template(
        'confirmation.html',
        message=message
    )

@app.route('/admin/courses/create-course')
def create_course():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')


    return render_template(
        'create-course.html',
    )

