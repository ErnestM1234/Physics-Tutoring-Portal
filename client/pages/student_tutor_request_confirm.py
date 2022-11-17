import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/student/tutor/request/confirm')
def student_tutor_request_confirm():

     # TO CHANGE
    course_id = request.args.get('course_id')
    tutor_id = request.args.get('tutor_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is student
    if "id" not in user.keys() or user['is_student'] == False:
        return redirect('/')



     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id})
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": tutor_id})
    tutor = res.json()

    requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps({'tutor_id': tutor_id, 'course_id': course_id, 'student_id': userId, 'status': 'REQUESTED'}))

    return render_template(
        'student-tutor-request-confirm.html',
        user=user,
        course=course,
        tutor=tutor
    )
