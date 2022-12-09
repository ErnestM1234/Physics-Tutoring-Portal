import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template
from pages.shared.get_user import *

load_dotenv()

# quick note: this displays tutorships, for some reason??
@app.route('/admin/students/')
def admin_students():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()
        
    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), headers=headers)
    tutorships = res.json()

    if res.status_code != 200:
        message = str(res)
        return render_template(
        'confirmation.html',
        message=message
    )

    for tutorship in tutorships:
        # TODO: implement a faster way of doing this (python lists have O(1) look up time)
        
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('student_id')}, headers=headers)
        student = res.json()
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('tutor_id')}, headers=headers)
        tutor = res.json()
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship.get('course_id')}, headers=headers)
        course = res.json()

        if not student or 'id' not in student.keys() or not tutor  or 'id' not in tutor.keys() or not course  or 'id' not in course.keys():
            return render_template(
                'confirmation.html',
                message="There is a missing tutor or course associated with this user!"
            )


        tutorship['student'] = student
        tutorship['tutor'] = tutor
        tutorship['course'] = course

    
    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'is_student': True}, headers=headers)
    students = res.json()  


    return render_template(
        'admin-students.html',
        tutorships=tutorships,
        students=students
    )
