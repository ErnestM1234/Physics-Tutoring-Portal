import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/student/tutors/request/confirm')
def student_tutors_request_confirm():

     # TO CHANGE
    course_id = request.args.get('course_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is student
    if "id" not in user.keys() or user['is_student'] == False:
        return redirect('/')



     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id})
    course = res.json()

    # get all tutors for that course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses'), params={"course_id": course_id})
    
    tutor_courses = res.json()

    # TO DO: PRUNE DUPLICATES
    # TO DO: DO NOT REQUEST UNAVAILABLE TUTORS
    for tutor_course in tutor_courses:
        #res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships'), params={"student_id": userId, "tutor_id": tutor_course['tutor_id'], "course_id": course_id})
        #tutorships = res.json()

        #if len(tutorships) == 0:
        #    requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps({'tutor_id': tutor_course['tutor_id'], 'course_id': course_id, 'student_id': userId, 'status': 'REQUESTED'}))
        
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps({'tutor_id': tutor_course['tutor_id'], 'course_id': course_id, 'student_id': userId, 'status': 'REQUESTED'}))

    return redirect('/student/dashboard')
    #return render_template(
    #    'student-tutors-request-confirm.html',
    #    user=user,
    #    course=course
    #)
