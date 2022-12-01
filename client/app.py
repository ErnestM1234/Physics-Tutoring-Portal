# run the following command to start the server: $ gunicorn app:app

import os
import flask
from flask import Flask, render_template, redirect
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    # todo: should this autoroute to one of the three dashboards??

    # request list of users
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    res2 = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'))
    res3 = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))

    data = res.json()
    data2 = res2.json()
    data3 = res3.json()
    # return 'hi'
    return render_template(
        'users.html',
        users=data,
        tutorships=data2,
        courses=data3
    )

@app.route('/dashboard')
def dashboard():

    student_tutorships = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={"id": 1})
    student_tutorships = student_tutorships.json()

    tutors = []

    for tutorship in student_tutorships:
        tutor_id = tutorship["tutor_id"]
        student_tutors = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={"id": tutor_id})
        student_tutors = student_tutors.json()
        tutors.append(student_tutors)

    print("-------------------")
    print(tutors)

    return render_template(
        'dashboard.html',
        tutors = tutors
    )








@app.route('/tutordashboard')
def tutor_dashboard():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    tutor_id = 1
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_id})
    tutor = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'tutor_id': tutor_id})
    tutor_courses = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'tutor_id': tutor_id})
    tutorships = res.json()


    for tutorship in tutorships:
        student_id = tutorship['student_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': student_id})
        student = res.json()
        tutorship['student'] = student

        course_id = tutorship['course_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id})
        course = res.json()
        tutorship['course'] = course
   
    for tutor_course in tutor_courses:
        course_id = tutor_course['course_id']
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id})
        course = res.json()
        tutor_course['course'] = course

    
    accepted_tutorships = list(filter(lambda tutorship: tutorship['status'] == 'ACCEPTED', tutorships))
    requested_tutorships = list(filter(lambda tutorship: tutorship['status'] == 'REQUESTED', tutorships))



    return render_template(
        'tutordash.html', tutor=tutor, accepted_tutorships=accepted_tutorships, requested_tutorships=requested_tutorships, tutor_courses = tutor_courses
    )

@app.route('/allclasses')
def allClasses():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))
    courses = res.json()
   
    return render_template(
        'allclasses.html', courses=courses
    )

@app.route('/editbio')
def editBio():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    tutor_id = 1
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_id})
    tutor = res.json()

    return render_template(
        'editbio.html', tutor=tutor
    )

@app.route('/tutorapplication')
def tutorApplication():
    
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))
    courses = res.json()

    tutor_id = 1
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_id})
    tutor = res.json()

    return render_template(
        'tutor-application.html', courses=courses, tutor=tutor
    )



@app.route('/editbio/confirm', methods=['POST'])
def edit_bio_confirm():

    bio = request.form.get('bio')
    tutor_id = request.form.get('tutor_id')

    if bio is None or tutor_id is None:
        return redirect('/editbio')

   
    data = {
        'bio': bio,
        'id': tutor_id
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps(data))
   
    message = str(res)


    return render_template(
        'confirmationtutor.html',
        message=message
    )



@app.route('/tutorapplication/confirm', methods=['POST'])
def tutor_application_confirm():

    tutor_id = request.form.get('tutor_id')
    name = request.form.get('name')
    email = request.form.get('email')
    netid = request.form.get('netid')
    course_name = request.form.get('course_name')
    taken_course = request.form.get('taken_course')
    experience = request.form.get('experience')

   
    data = {
        'id': tutor_id,
        'name': name,
        'email': email, 
        'netid': netid, 
        'course_name': course_name, 
        'taken_course': taken_course, 
        'experience': experience
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps(data))
   
    message = str(res)


    return render_template(
        'confirmationtutor.html',
        message=message
    )


@app.route('/tutor/student/dissolve')
def tutor_student_dissolve():

    # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id})
    student = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id})
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    tutor = res.json()

    return render_template(
        'tutor-student-dissolve.html',
        student=student,
        course=course,
        tutor=tutor
    )

@app.route('/tutor/student/dissolve/confirm')
def tutor_student_dissolve_confirm():

     # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id})
    student = res.json()


     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id})
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    tutor = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id, 'tutor_id': userId, 'course_id': course_id})
    tutorship = res.json()
    
    print("len")
    print(len(tutorship))
    print("tutorship")
    print(tutorship)

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/delete/'), data=json.dumps({'id': tutorship['id']}))

    return render_template(
        'tutor-student-dissolve-confirm.html',
        student=student,
        course=course,
        tutor=tutor
    )


@app.route('/tutor/student/accept')
def tutor_student_accept():

    # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id})
    student = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id})
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    tutor = res.json()

    return render_template(
        'tutor-student-accept.html',
        student=student,
        course=course,
        tutor=tutor
    )

@app.route('/tutor/student/accept/confirm')
def tutor_student_accept_confirm():

     # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id})
    student = res.json()


     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id})
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    tutor = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id, 'tutor_id': userId, 'course_id': course_id})
    tutorship = res.json()
    

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/update'), data=json.dumps({'id': tutorship['id'], 'status': 'ACCEPTED'}))

    return render_template(
        'tutor-student-accept-confirm.html',
        student=student,
        course=course,
        tutor=tutor
    )



@app.route('/tutor/student/reject')
def tutor_student_reject():

    # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id})
    student = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id})
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    tutor = res.json()

    return render_template(
        'tutor-student-reject.html',
        student=student,
        course=course,
        tutor=tutor
    )

@app.route('/tutor/student/reject/confirm')
def tutor_student_reject_confirm():

     # TO CHANGE
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": student_id})
    student = res.json()


     # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={"id": course_id})
    course = res.json()

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    tutor = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id, 'tutor_id': userId, 'course_id': course_id})
    tutorship = res.json()
    

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]
        requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/update'), data=json.dumps({'id': tutorship['id'], 'status': 'BLOCKED'}))

    return render_template(
        'tutor-student-reject-confirm.html',
        student=student,
        course=course,
        tutor=tutor
    )


















# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
# pylint: disable-next=unused-wildcard-import
# pylint: disable-next=wildcard-import
from pages.admin_dashboard import *
from pages.admin_courses import *
from pages.admin_tutorships import *
from pages.admin_tutors import *
from pages.admin_students import *
from pages.admin_admins import *
from pages.create_course import *
from pages.create_tutor_course import *
from pages.create_tutorship import *
from pages.create_user import *
from pages.remove_course import *
from pages.remove_tutorship import *
from pages.student_profile import *
from pages.tutor_profile import *


from pages.student_dashboard import *
from pages.student_courses import *
from pages.student_course import *
from pages.student_tutor import *
from pages.student_tutor_request import *
from pages.student_tutor_cancel import *
from pages.student_tutor_dissolve import *
from pages.student_tutor_request_confirm import *
from pages.student_tutor_cancel_confirm import *
from pages.student_tutor_dissolve_confirm import *

if __name__ == '__main__':
    app.run()