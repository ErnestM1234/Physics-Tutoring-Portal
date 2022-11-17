import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/student-profile/')
def student_profile():
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

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if "id" not in user.keys() or user['is_admin'] == False:
        return redirect('/')


    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id})
    student = res.json()
    # check if they are a student
    if "id" not in student.keys() or not student['is_student']:
        return render_template(
            'confirmation.html',
            message="This ID does not belong to a 'Student'"
        )

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id})
    tutorships = res.json()

    for tutorship in tutorships:
        # TODO: implement a faster way of doing this (python lists have O(1) look up time)
        
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('tutor_id')})
        tutor = res.json()
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship.get('course_id')})
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

