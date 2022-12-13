import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/tutorships/remove-tutorship/confirm/', methods=['GET'])
def remove_tutorship_confirm():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    tutorship_id = request.args.get('tutorship_id')
    if tutorship_id and tutorship_id.isnumeric() and int(float(tutorship_id)) >= 0:
        tutorship_id = int(float(tutorship_id))
    else:
        session['error_message'] = "There is no provided tutorship_id, or the tutorship_id is invalid"
        return redirect('/error/')

    # remove tutorship
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/delete/'), data=json.dumps({'id': tutorship_id}), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    return redirect('/admin/tutorships/')

@app.route('/admin/tutorships/remove-tutorship/')
def remove_tutorship():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    tutorship_id = request.args.get('tutorship_id')
    if tutorship_id and tutorship_id.isnumeric() and int(float(tutorship_id)) >= 0:
        tutorship_id = int(float(tutorship_id))
    else:
        session['error_message'] = "There is no provided tutorship_id, or the tutorship_id is invalid"
        return redirect('/error/')
    

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorship/'), params={'id': tutorship_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorship = res.json()
    if tutorship and 'id' not in tutorship.keys():
        session['error_message'] = str(res.content)
        return redirect('/error/')

    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('student_id')}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    student = res.json()
    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('tutor_id')}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor = res.json()
    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship.get('course_id')}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    course = res.json()


    tutorship['tutor'] = tutor
    tutorship['student'] = student
    tutorship['course'] = course

    if not student or 'id' not in student.keys() or not tutor or 'id' not in tutor.keys() or not course or 'id' not in course.keys():
        session['error_message'] = "There is a missing student or course associated with this tutorship!"
        return redirect('/error/')


    return render_template(
        '/admin/admin-remove-tutorship.html',
        tutorship=tutorship
    )

