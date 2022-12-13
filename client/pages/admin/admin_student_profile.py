import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *

load_dotenv()

@app.route('/admin/student-profile/')
def student_profile():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    # param validation
    student_id = request.args.get('student_id')
    tutorship_params = {"id": None}
    if student_id is not None:
        if student_id.isnumeric() and int(float(student_id)) >= 0:
            tutorship_params['id'] = int(float(student_id))
        else:
            session['error_message'] = "You have supplied an invalid user id"
            return redirect('/error/')
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": user.id}, headers=headers)
    user = res.json()
    # verify is admin
    if "id" not in user.keys() or user['is_admin'] == False:
        return redirect('/')


    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id}, headers=headers)
    student = res.json()
    # check if they are a student
    if "id" not in student.keys() or not student['is_student']:
        session['error_message'] = "This ID does not belong to a 'Student'"
        return redirect('/error/')

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorships = res.json()


    for tutorship in tutorships:
        # TODO: implement a faster way of doing this (python lists have O(1) look up time)
        
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('tutor_id')}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        tutor = res.json()

        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship.get('course_id')}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        course = res.json()

        if not tutor or not course:
            session['error_message'] = "There is a missing tutor or course associated with this user!"
            return redirect('/error/')

        tutorship['tutor'] = tutor
        tutorship['course'] = course



    isAStudent = 'Is a Student'
    isATutor = 'Not a Tutor'
    isAnAdmin = 'Not an Admin'
        
    if(student['is_tutor']):
        isATutor = 'Is a Tutor'
    if(student['is_admin']):
        isAnAdmin = 'Is an Admin'
        


    return render_template(
        '/admin/admin-profile-student.html',
        user=user,
        student=student,
        tutorships=tutorships, 
        isATutor = isATutor, 
        isAnAdmin = isAnAdmin, 
        isAStudent = isAStudent
    )

