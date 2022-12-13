import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/admin/tutor-course/')
def tutor_course():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    # param validation
    tutor_course_id = request.args.get('tutor_course_id')


    if tutor_course_id is not None:
        if tutor_course_id.isnumeric() and int(float(tutor_course_id)) >= 0:
            tutor_course_id = int(float(tutor_course_id))
        else:
            session['error_message'] = "You have supplied an incorrect tutor course id"
            return redirect('/error/')

    # get tutor-course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/'), params={"id": tutor_course_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": tutor_course['tutor_id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor = res.json()



    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutor_course.get('course_id')}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    course = res.json()
    tutor_course['course'] = course

 
    return render_template(
        '/admin/admin-tutor-course.html',
        user=user,
        tutor=tutor,
        tutor_course=tutor_course
    )

