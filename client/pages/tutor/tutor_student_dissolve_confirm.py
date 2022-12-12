import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/tutor/student/dissolve/confirm')
def tutor_student_dissolve_confirm():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


     # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()


     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user['id']}, headers=headers)
    tutor = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id, 'tutor_id': user['id'], 'course_id': course_id}, headers=headers)
    tutorship = res.json()
    
    print("len")
    print(len(tutorship))
    print("tutorship")
    print(tutorship)

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/delete/'), data=json.dumps({'id': tutorship['id']}), headers=headers)

    return render_template(
        '/tutor/tutor-student-dissolve-confirm.html',
        student=student,
        course=course,
        tutor=tutor, 
        user=user
    )
