import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

def get_name(id):
    # this is very slow!! replace this!!
    headers = get_header()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": id}, headers=headers)
    user = res.json()
    # verify is admin
    if 'id' not in user.keys():
        return redirect('/')
    return user['name']

@app.route('/admin/course/')
def admin_course():
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
    course_id = request.args.get('course_id')
    tutorship_params = {"course_id": None}
    print(course_id)
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            tutorship_params['course_id'] = int(float(course_id))
            course_id = int(float(course_id))
        else:
            return redirect('/')
    
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
    course = res.json()

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params=tutorship_params, headers=headers)
    tutorships = res.json()

    print(tutorships)

    if res.status_code != 200:
        message = str(res)
        return render_template(
        '/admin/confirmation.html',
        message=message
    )



    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params=tutorship_params, headers=headers)
    tutor_courses = res.json()

    approved_tutor_courses = list(filter(lambda tutor_course: tutor_course['status'] == 'ACCEPTED', tutor_courses))


    student_count = []
    # todo: make a specific endpoint for this
    for tutor_course in approved_tutor_courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={"tutor_id": tutor_course['tutor_id']}, headers=headers)
        tutorships2 = res.json()
        student_count.append(len(tutorships2))

    tutor_requests = list(filter(lambda tutor_course: tutor_course['status'] == 'REQUESTED', tutor_courses))
    denied_tutors = list(filter(lambda tutor_course: tutor_course['status'] == 'DENIED', tutor_courses))


    if res.status_code != 200:
        message = str(res)
        return render_template(
        '/admin/confirmation.html',
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

        if not student or not tutor or not course:
            return render_template(
                '/admin/confirmation.html',
                message="There is a missing tutor or course associated with this user!"
            )


        tutorship['student'] = student
        tutorship['tutor'] = tutor
        tutorship['course'] = course

    return render_template(
        '/admin/admin-course.html',
        tutorships=tutorships,
        course = course,
        course_id=course_id,
        tutor_courses=approved_tutor_courses,
        student_count=student_count,
        tutor_requests= tutor_requests,
        denied_tutors= denied_tutors,
        get_name=get_name,
    )


