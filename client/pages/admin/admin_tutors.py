from collections import OrderedDict
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
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            course_id = int(float(course_id))
        else:
            session['error_message'] = "You have supplied an incorrect course id"
            return redirect('/error/')


    # get course if course_id is supplied
    course = None
    if course_id:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": str(course_id)}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        course = res.json()

    # get tutor_courses (deep) (this means include course and tutor)
    tutor_course_params = {}
    if course_id is not None:
        tutor_course_params['course_id'] = course_id
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/deep/'), params=tutor_course_params, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_courses = res.json()

    # get list of accepted tutor courses
    approved_tutor_courses = list(filter(lambda _tutor_course: _tutor_course['status'] in ['ACCEPTED', 'UNAVAILABLE'], tutor_courses))
    # get list of tutor_course requests
    tutor_requests = list(filter(lambda tutor_course: tutor_course['status'] == 'REQUESTED', tutor_courses))

    # get a list of approved tutors (associated with the given course)
    approved_tutors = [approved_tutor_course["tutor"] for approved_tutor_course in approved_tutor_courses]
    approved_tutors = [dict(t) for t in {tuple(d.items()) for d in approved_tutors}] # remove duplicates


    # get counts for accepted tutorships (requested/denied tutors have counts = 0)
    tutorship_count_params = {
        "ids": [tutor['id'] for tutor in approved_tutors],
        "status": 'ACCEPTED',
    }
    if course_id is not None:
        tutorship_count_params['course_id'] = course_id
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/tutorship_count'), params=tutorship_count_params, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    counts = res.json()
    for tutor in approved_tutors:
        tutor["tutorship_count"] = counts[str(tutor['id'])]


    return render_template(
        '/admin/admin-tutors.html',
        course=course,
        user=user,
        approved_tutor_courses = approved_tutor_courses, 
        tutor_requests=tutor_requests, 
        get_name = get_name, 
        tutors=approved_tutors
    )

