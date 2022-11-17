import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/tutorships/create-tutorship/confirm', methods=['POST'])
def create_tutorship_confirm():

    student_id = request.form.get('student_id')
    tutor_id = request.form.get('tutor_id')
    course_id = request.form.get('course_id')
    status = request.form.get('status')

    if student_id is None or tutor_id is None or course_id is None or status is None:
        return redirect('/')

    
    data = {
        'student_id': student_id,
        'tutor_id': tutor_id,
        'course_id': course_id,
        'status': status,
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps(data))
    
    message = str(res)


    return render_template(
        'confirmation.html',
        message=message
    )

@app.route('/admin/tutorships/create-tutorship/')
def create_tutorship():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')


    return render_template(
        'create-tutorship.html',
    )

