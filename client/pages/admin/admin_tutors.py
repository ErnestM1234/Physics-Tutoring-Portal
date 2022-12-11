import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *

load_dotenv()

@app.route('/admin/tutors/update_status', methods=['POST'])
def set_tutor_course_status():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    tutor_course_id = request.form.get('tutor_course_id')
    status = request.form.get('status')
    # param validation
    if int(float(tutor_course_id)) >= 0:
        validated_tutor_course_id = int(float(tutor_course_id))
    else:
        return redirect('/')

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/update'), data=json.dumps({"id": str(validated_tutor_course_id), "status": status}), headers=headers)

    return str(res)



def get_name(id):
    # this is very slow!! replace this!!
    headers = get_header()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": id}, headers=headers)
    user = res.json()
    # verify is admin
    if 'id' not in user.keys():
        return redirect('/')
    return user['name']

@app.route('/admin/tutors/')
def admin_tutors():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    # param validation
    course_id = request.args.get('course_id')
    tutor_course_params = {"course_id": None}
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            tutor_course_params['course_id'] = int(float(course_id))
            course_id = int(float(course_id))
        else:
            return redirect('/') # TODO: change this to an error message


    #added this: 
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
    course = res.json()

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params=tutor_course_params, headers=headers)
    tutor_courses = res.json()

    approved_tutor_courses = list(filter(lambda tutor_course: tutor_course['status'] == 'ACCEPTED', tutor_courses))


    student_count = []
    # todo: make a specific endpoint for this
    for tutor_course in approved_tutor_courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={"tutor_id": tutor_course['tutor_id']}, headers=headers)
        tutorships = res.json()
        student_count.append(len(tutorships))

    tutor_requests = list(filter(lambda tutor_course: tutor_course['status'] == 'REQUESTED', tutor_courses))
    denied_tutors = list(filter(lambda tutor_course: tutor_course['status'] == 'DENIED', tutor_courses))


    return render_template(
        '/admin/admin-tutors.html',
        tutor_courses=approved_tutor_courses,
        student_count=student_count,
        tutor_requests=tutor_requests,
        denied_tutors=denied_tutors,
        get_name=get_name,
        course_id=course_id, 
        course = course
    )

