import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/tutorships/')
def admin_tutorships():
    # param validation
    course_id = request.args.get('course_id')
    tutorship_params = {"course_id": None}
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            tutorship_params['course_id'] = int(float(course_id))
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
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params=tutorship_params)
    tutorships = res.json()

    for tutorship in tutorships:
        # TODO: implement a faster way of doing this (python lists have O(1) look up time)
        
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('student_id')})
        student = res.json()
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('tutor_id')})
        tutor = res.json()
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship.get('course_id')})
        course = res.json()

        if not student or not tutor or not course:
            return render_template(
                'confirmation.html',
                message="There is a missing tutor or course associated with this user!"
            )


        tutorship['student'] = student
        tutorship['tutor'] = tutor
        tutorship['course'] = course

    return render_template(
        'admin-tutorships.html',
        tutorships=tutorships,
        course_id=course_id
    )

