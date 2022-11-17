import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/create-tutor-course/confirm', methods=['POST'])
def create_tutor_course_confirm():

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



    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/create'), data=json.dumps(data))
    
    message = str(res)
    print(res.content)


    return render_template(
        'confirmation.html',
        message=message
    )

@app.route('/admin/create-tutor-course')
def create_tutor_course():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')


    return render_template(
        'create-tutor-course.html',
    )

