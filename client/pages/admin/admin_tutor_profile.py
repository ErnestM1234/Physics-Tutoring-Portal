import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/admin/tutor-profile/')
def tutor_profile():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    # param validation
    tutor_id = request.args.get('tutor_id')

    tutorship_params = {"id": None}
    if tutor_id is not None:
        if tutor_id.isnumeric() and int(float(tutor_id)) >= 0:
            tutorship_params['id'] = int(float(tutor_id))
        else:
            return render_template(
            '/admin/confirmation.html',
            message="You have supplied an invalid user id"
        )





    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": tutor_id}, headers=headers)
    tutor = res.json()
    # check if they are a tutor
    if res.status_code != 200:
        return render_template(
            '/admin/confirmation.html',
            message="User not found"
        )

    # get tutor-courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'tutor_id': tutor_id}, headers=headers)
    tutor_courses = res.json()

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'tutor_id': tutor_id}, headers=headers)
    tutorships = res.json()

    for tutor_course in tutor_courses:
        # get tutorship count (number of students that the tutor is tutoring) by class
        student_count = len(list(filter(lambda tutorship: tutorship['status'] == 'ACCEPTED' and tutorship['course_id'] == tutor_course['course_id'] and tutor_course['status'] == "ACCEPTED", tutorships)))
        tutor_course["student_count"] = student_count


        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutor_course.get('course_id')}, headers=headers)
        course = res.json()
        tutor_course['course'] = course

    



    return render_template(
        '/admin/admin-profile-tutor.html',
        tutor=tutor,
        tutor_courses=tutor_courses
    )

