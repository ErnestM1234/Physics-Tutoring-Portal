
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/tutors/request/confirm')
def student_tutors_request_confirm():

     # TO CHANGE
    course_id = request.args.get('course_id')

    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            '/student/student-no-access.html',
            message='you do not have permission to access this page'
        )
    
    # get headers
    headers = get_header()


     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id}, headers=headers)
    course = res.json()

    # get all tutors for that course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses'), params={"course_id": course_id}, headers=headers)
    
    tutor_courses = res.json()

    # TO DO: PRUNE DUPLICATES
    # TO DO: DO NOT REQUEST UNAVAILABLE TUTORS
    for tutor_course in tutor_courses:
        #res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships'), params={"student_id": userId, "tutor_id": tutor_course['tutor_id'], "course_id": course_id})
        #tutorships = res.json()

        #if len(tutorships) == 0:
        #    requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps({'tutor_id': tutor_course['tutor_id'], 'course_id': course_id, 'student_id': userId, 'status': 'REQUESTED'}))
        
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps({'tutor_id': tutor_course['tutor_id'], 'course_id': course_id, 'student_id': user['id'], 'status': 'REQUESTED'}), headers=headers)

    return redirect('/student/dashboard')
    #return render_template(
    #    'student-tutors-request-confirm.html',
    #    user=user,
    #    course=course
    #)
