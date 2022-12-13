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
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    tutor_course_id = request.form.get('tutor_course_id')
    status = request.form.get('status')
    # param validation
    if tutor_course_id.isnumeric() and int(float(tutor_course_id)) >= 0:
        validated_tutor_course_id = int(float(tutor_course_id))
    else:
        session['error_message'] = "You have supplied an incorrect tutor course id"
        return redirect('/error/')

        


    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/update'), data=json.dumps({"id": str(validated_tutor_course_id), "status": status}), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    return str(res)



def get_name(id):
    # this is very slow!! replace this!!
    headers = get_header()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    user = res.json()

    if 'id' not in user.keys():
        session['error_message'] = "You have supplied an incorrect user id"
        return redirect('/error/')
    return user['name']

@app.route('/admin/tutors/')
def admin_tutors():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    # param validation
    course_id = request.args.get('course_id')
    tutor_course_params = {"course_id": None}
    course = None
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            tutor_course_params['course_id'] = int(float(course_id))
            course_id = int(float(course_id))
        else:
            session['error_message'] = "You have supplied an incorrect course id"
            return redirect('/error/')

        #added this: 
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        course = res.json()

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params=tutor_course_params, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_courses = res.json()

    for tutor_course in tutor_courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutor_course['course_id']}, headers=headers)
        course2 = res.json()
        course2_name = course2['name']
        tutor_course['course_name']= course2_name

    approved_tutor_courses = list(filter(lambda tutor_course: tutor_course['status'] == 'ACCEPTED', tutor_courses))


    student_count = []
    # todo: make a specific endpoint for this
    for tutor_course in approved_tutor_courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={"tutor_id": tutor_course['tutor_id']}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        tutorships = res.json()
        student_count.append(len(tutorships))
        





    tutor_requests = list(filter(lambda tutor_course: tutor_course['status'] == 'REQUESTED', tutor_courses))
    denied_tutors = list(filter(lambda tutor_course: tutor_course['status'] == 'DENIED', tutor_courses))


    return render_template(
        '/admin/admin-tutors.html',
        user=user,
        tutor_courses=approved_tutor_courses,
        student_count=student_count,
        tutor_requests=tutor_requests,
        denied_tutors=denied_tutors,
        get_name=get_name,
        course_id=course_id, 
        course=course
    )

