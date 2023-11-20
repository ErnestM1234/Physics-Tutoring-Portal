import json
from math import isnan
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/tutors/update-tutor/confirm', methods=['GET'])
def update_tutor_course_confirm():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    # get parametes
    tutor_id = request.args.get('tutor_id')
    tutor_course_id = request.args.get('tutor_course_id')
    status = str(request.args.get('status'))
    if tutor_id is None or tutor_id == "" or tutor_course_id is None or tutor_course_id == '' or status is None or status not in ['DENIED', 'UNAVAILABLE', 'ACCEPTED', 'REQUESTED']:
        session['error_message'] = 'Invalid arguments'
        return redirect('/error/')
    try:
        tutor_course_id = int(float(tutor_course_id))
    except:
        session['error_message'] = 'Invalid arguments'
        return redirect('/error/')

    # remove tutorships
    if status == 'DENIED' or status == 'REQUESTED':
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/'), params={'id': tutor_course_id}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        tutor_course = res.json()
        if 'id' not in tutor_course.keys():
            session['error_message'] = 'something went wrong'
            return redirect('/error/')

        course_id = tutor_course['course_id']

        # get tutorships
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'tutor_id': tutor_id, 'course_id': course_id}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        tutorships = res.json()
        if not isinstance(tutorships, list):
            session['error_message'] = 'something went wrong'
            return redirect('/error/')

        # remove tutorships
        for tutorship in tutorships:
            res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/delete/'), data=json.dumps({'id': tutorship['id']}), headers=headers)
            if res.status_code != 200:
                session['error_message'] = str(res.content)
                return redirect('/error/')

    # update status
    data = {
        'id': tutor_course_id,
        'status': status
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/update/'), data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    
    return redirect('/admin/tutor-profile/?tutor_id=' + str(tutor_id))

@app.route('/admin/tutors/update-tutor')
def update_tutor_course():

    # verify is admin
    user = get_user(requests)
    if "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')

    # get headers
    headers = get_header()

    # get parameters
    tutor_id = request.args.get('tutor_id')
    tutor_course_id = request.args.get('tutor_course_id')
    status = str(request.args.get('status'))
    if tutor_id is None or tutor_id == "" or tutor_course_id is None or tutor_course_id == '' or status is None or status not in ['DENIED', 'UNAVAILABLE', 'ACCEPTED', 'REQUESTED']:
        session['error_message'] = 'Invalid arguments'
        return redirect('/error/')
    try:
        tutor_course_id = int(float(tutor_course_id))
    except:
        session['error_message'] = 'Invalid arguments'
        return redirect('/error/')

    # get tutor course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/'), params={'id': tutor_course_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_course = res.json()
    if 'id' not in tutor_course.keys():
        session['error_message'] = 'something went wrong'
        return redirect('/error/')

    course_id = tutor_course['course_id']

    
    # get tutorships
    tutorship_count = 0
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'tutor_id': tutor_id, 'course_id': course_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorships = res.json()
    if not isinstance(tutorships, list):
        session['error_message'] = 'something went wrong'
        return redirect('/error/')
    tutorship_count=len(tutorships)

    return render_template(
        '/admin/admin-update-tutor-course.html',
        user=user,
        tutor_course_id=tutor_course_id,
        status=status,
        tutor_id=tutor_id,
        tutorship_count=tutorship_count
    )

