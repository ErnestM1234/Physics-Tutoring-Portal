import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/tutor-profile/')
def tutor_profile():
    # param validation
    tutor_id = request.args.get('tutor_id')
    tutorship_params = {"id": None}
    if tutor_id is not None:
        if tutor_id.isnumeric() and int(float(tutor_id)) >= 0:
            tutorship_params['id'] = int(float(tutor_id))
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


    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": tutor_id})
    tutor = res.json()
    # check if they are a tutor
    if "id" not in tutor.keys() or not tutor['is_tutor']:
        return render_template(
            'confirmation.html',
            message="This ID does not belong to a 'Tutor'"
        )

    # get tutor-courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'tutor_id': tutor_id})
    tutor_courses = res.json()

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'tutor_id': tutor_id})
    tutorships = res.json()

    for tutor_course in tutor_courses:
        # get tutorship count (number of students that the tutor is tutoring) by class
        student_count = len(list(filter(lambda tutorship: tutorship['status'] == 'ACCEPTED' and tutorship['course_id'] == tutor_course['course_id'] and tutor_course['status'] == "ACCEPTED", tutorships)))
        tutor_course["student_count"] = student_count


        # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutor_course.get('course_id')})
        # course = res.json()
        # tutor_course['course'] = course




    return render_template(
        'profile-tutor.html',
        tutor=tutor,
        tutor_courses=tutor_courses
    )

