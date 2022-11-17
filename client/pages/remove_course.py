import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/courses/remove-course/confirm/', methods=['GET'])
def remove_user_confirm():

    course_id = request.args.get('course_id')
    if course_id and course_id.isnumeric() and int(float(course_id)) >= 0:
        course_id = int(float(course_id))
    else:
        return render_template(
            'confirmation.html',
            message="There is no provided course_id, or the course_id is invalid"
        )

    # TODO: set up an endpoint
    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'course_id': course_id})
    tutorships = res.json()
    if not isinstance(tutorships, list):
        print(str(res.content))
        return render_template(
            'confirmation.html',
            message=str(tutorships)
        )
    # remove tutorships
    for tutorship in tutorships:
        res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/delete/'), data=json.dumps({'id': tutorship['id']}))
        if res.status_code != 200:
            print(str(res.content))
            return render_template(
            'confirmation.html',
            message=str(res)
        )

    # TODO: set up an endpoint
    # get tutor_courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'course_id': course_id})
    tutor_courses = res.json()
    if not isinstance(tutorships, list):
        print(str(res.content))
        return render_template(
            'confirmation.html',
            message=str(tutor_courses)
        )
    # remove tutor_courses
    for tutor_course in tutor_courses:
        res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/delete/'), data=json.dumps({'id': tutor_course['id']}))
        tutorships = res.json()
        if res.status_code != 200:
            print(str(res.content))
            return render_template(
            'confirmation.html',
            message=str(res)
        )


    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/course/delete/'), data=json.dumps({'id': course_id }))
    
    message = str(res)

    return render_template(
        'confirmation.html',
        message=message
    )

@app.route('/admin/courses/remove-course/')
def remove_course():
    course_id = request.args.get('course_id')
    if course_id and course_id.isnumeric() and int(float(course_id)) >= 0:
        course_id = int(float(course_id))
    else:
        return render_template(
            'confirmation.html',
            message="There is no provided course_id, or the course_id is invalid"
        )


    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')
    

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'course_id': course_id})
    tutorships = res.json()
    if not isinstance(tutorships, list):
        return render_template(
            'confirmation.html',
            message=str(tutorships)
        )

    # get course_tutors
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'course_id': course_id})
    course_tutors = res.json()
    if not isinstance(tutorships, list):
        return render_template(
            'confirmation.html',
            message=str(course_tutors)
        )


    return render_template(
        'remove-course.html',
        course_id=course_id,
        tutorship_count=len(tutorships),
        tutor_course_count=len(course_tutors)
    )

