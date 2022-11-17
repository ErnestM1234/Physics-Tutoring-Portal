
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/student/course')
def student_course():

    # TO CHANGE
    course_id = request.args.get('id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is student
    if "id" not in user.keys() or user['is_student'] == False:
        return redirect('/')

    # get approved tutors
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'course_id': course_id, 'status': 'ACCEPTED'})
    tutor_courses = res.json()

    for tutor_course in tutor_courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_course['tutor_id']})
        tutor = res.json()
        tutor_course['tutor'] = tutor

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id})
    course = res.json()

    return render_template(
        'student-course.html',
        user=user,
        tutor_courses=tutor_courses,
        course=course
    )
