import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/tutorship/')
def admin_tutorship():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    # param validation


    tutorship_id = request.args.get('tutorship_id')

    if tutorship_id is not None:
        if tutorship_id.isnumeric() and int(float(tutorship_id)) >= 0:
            tutorship_id = int(float(tutorship_id))
        else:
            session['error_message'] = "You have supplied an incorrect tutorship id"
            return redirect('/error/')


    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'id': tutorship_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorship = res.json()
    tutorship = tutorship[0]

    print(tutorship)

        
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship['student_id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    student = res.json()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship['tutor_id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor = res.json()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship['course_id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    course = res.json()

    if not student or not tutor or not course:
        session['error_message'] = "There is a missing tutor or course associated with this user!"
        return redirect('/error/')


    tutorship['student'] = student
    tutorship['tutor'] = tutor
    tutorship['course'] = course

    return render_template(
        '/admin/admin-tutorship.html',
        tutorship=tutorship,
        course = course, 
        user=user
    )