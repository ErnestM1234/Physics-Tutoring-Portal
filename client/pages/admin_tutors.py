import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/tutors/update_status', methods=['POST'])
def set_tutor_course_status():
    # TODO: this is not secure at all! anyone can invoke this method!
    tutor_course_id = request.form.get('tutor_course_id')
    status = request.form.get('status')
    # param validation
    if int(float(tutor_course_id)) >= 0:
        validated_tutor_course_id = int(float(tutor_course_id))
    else:
        return redirect('/')

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/update'), data=json.dumps({"id": str(validated_tutor_course_id), "status": status}))

    return str(res)



def get_name(id):
    # this is very slow!! replace this!!
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": id})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys():
        return redirect('/')
    return user['name']

@app.route('/admin/tutors/')
def admin_tutors():
    # param validation
    course_id = request.args.get('course_id')
    tutor_course_params = {"course_id": None}
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            tutor_course_params['course_id'] = int(float(course_id))
            course_id = int(float(course_id))
        else:
            return redirect('/')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params=tutor_course_params)
    tutor_courses = res.json()

    approved_tutor_courses = list(filter(lambda tutor_course: tutor_course['status'] == 'APPROVED', tutor_courses))


    student_count = []
    # todo: make a specific endpoint for this
    for tutor_course in approved_tutor_courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={"tutor_id": tutor_course['tutor_id']})
        tutorships = res.json()
        student_count.append(len(tutorships))

    tutor_requests = list(filter(lambda tutor_course: tutor_course['status'] == 'REQUESTED', tutor_courses))
    denied_tutors = list(filter(lambda tutor_course: tutor_course['status'] == 'DENIED', tutor_courses))


    return render_template(
        'admin-tutors.html',
        tutor_courses=approved_tutor_courses,
        student_count=student_count,
        tutor_requests=tutor_requests,
        denied_tutors=denied_tutors,
        get_name=get_name,
        course_id=course_id
    )

