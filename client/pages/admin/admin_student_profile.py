import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/admin/student-profile/')
def student_profile():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    # param validation
    student_id = request.args.get('student_id')
    tutorship_params = {"id": None}
    if student_id is not None:
        if student_id.isnumeric() and int(float(student_id)) >= 0:
            tutorship_params['id'] = int(float(student_id))
        else:
            return render_template(
            'confirmation.html',
            message="You have supplied an invalid user id"
        )


    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()
    # check if they are a student
    if "id" not in student.keys() or not student['is_student']:
        return render_template(
            'confirmation.html',
            message="This ID does not belong to a 'Student'"
        )

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id}, headers=headers)
    tutorships = res.json()

    for tutorship in tutorships:
        # TODO: implement a faster way of doing this (python lists have O(1) look up time)
        
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('tutor_id')}, headers=headers)
        tutor = res.json()
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship.get('course_id')}, headers=headers)
        course = res.json()

        if not tutor or not course:
            return render_template(
                'confirmation.html',
                message="There is a missing tutor or course associated with this user!"
            )

        tutorship['tutor'] = tutor
        tutorship['course'] = course



    return render_template(
        'profile-student.html',
        student=student,
        tutorships=tutorships
    )
