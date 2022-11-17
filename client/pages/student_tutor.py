
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/student/tutor')
def student_tutor():

    # TO CHANGE
    tutor_id = request.args.get('tutor_id')
    course_id = request.args.get('course_id')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is student
    if "id" not in user.keys() or user['is_student'] == False:
        return redirect('/')

    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutor_id})
    tutor = res.json()

    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id})
    course = res.json()

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': userId, 'tutor_id': tutor_id, 'course_id': course_id})
    tutorship = res.json()

    if len(tutorship) == 0:
        tutorship = None
    else:
        tutorship=tutorship[0]

    return render_template(
        'student-tutor.html',
        user=user,
        tutor=tutor,
        course=course,
        tutorship = tutorship
    )
