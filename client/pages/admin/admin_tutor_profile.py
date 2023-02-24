import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/admin/tutor-profile/')
def tutor_profile():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    # param validation
    tutor_id = request.args.get('tutor_id')

    tutorship_params = {"id": None}
    if tutor_id is not None:
        if tutor_id.isnumeric() and int(float(tutor_id)) >= 0:
            tutorship_params['id'] = int(float(tutor_id))
        else:
            session['error_message'] = "You have supplied an invalid user id"
            return redirect('/error/')

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": tutor_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor = res.json()

    # get tutor-courses (deep)
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/deep/'), params={'tutor_id': tutor_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_courses = res.json()

    isAStudent = 'Is a Student'
    isATutor = 'Not a Tutor'
    isAnAdmin = 'Not an Admin'
        
    if(tutor['is_tutor']):
        isATutor = 'Is a Tutor'
    if(tutor['is_admin']):
        isAnAdmin = 'Is an Admin'

 
    return render_template(
        '/admin/admin-profile-tutor.html',
        user=user,
        tutor=tutor,
        tutor_courses=tutor_courses, 
        isATutor=isATutor, 
        isAnAdmin=isAnAdmin, 
        isAStudent=isAStudent
    )

