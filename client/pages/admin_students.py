import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template

load_dotenv()

# quick note: this displays tutorships, for some reason??
@app.route('/admin/students/')
def admin_students():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if "id" not in user.keys() or user['is_admin'] == False:
        return redirect('/')
        
    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'))
    tutorships = res.json()

    if res.status_code != 200:
        message = str(res)
        return render_template(
        'confirmation.html',
        message=message
    )

    for tutorship in tutorships:
        # TODO: implement a faster way of doing this (python lists have O(1) look up time)
        
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('student_id')})
        student = res.json()
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('tutor_id')})
        tutor = res.json()
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship.get('course_id')})
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
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'is_student': True})
    students = res.json()  


    return render_template(
        'admin-students.html',
        tutorships=tutorships,
        students=students
    )

