import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/tutorships/remove-tutorship/confirm/', methods=['GET'])
def remove_tutorship_confirm():

    tutorship_id = request.args.get('tutorship_id')
    if tutorship_id and tutorship_id.isnumeric() and int(float(tutorship_id)) >= 0:
        tutorship_id = int(float(tutorship_id))
    else:
        return render_template(
            'confirmation.html',
            message="There is no provided tutorship_id, or the tutorship_id is invalid"
        )

    # remove tutorship
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/delete/'), data=json.dumps({'id': tutorship_id}))
    message = str(res)

    return render_template(
        'confirmation.html',
        message=message
    )

@app.route('/admin/tutorships/remove-tutorship/')
def remove_tutorship():
    tutorship_id = request.args.get('tutorship_id')
    if tutorship_id and tutorship_id.isnumeric() and int(float(tutorship_id)) >= 0:
        tutorship_id = int(float(tutorship_id))
    else:
        return render_template(
            'confirmation.html',
            message="There is no provided tutorship_id, or the tutorship_id is invalid"
        )


    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')
    

    # get tutorship
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorship/'), params={'id': tutorship_id})
    tutorship = res.json()
    if tutorship and 'id' not in tutorship.keys():
        return render_template(
            'confirmation.html',
            message=str(tutorship)
        )

    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('student_id')})
    student = res.json()
    # get tutor
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship.get('tutor_id')})
    tutor = res.json()
    # get course
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship.get('course_id')})
    course = res.json()


    tutorship['tutor'] = tutor
    tutorship['student'] = student
    tutorship['course'] = course

    if not student or 'id' not in student.keys() or not tutor or 'id' not in tutor.keys() or not course or 'id' not in course.keys():
        return render_template(
            'confirmation.html',
            message="There is a missing student or course associated with this tutorship!"
        )


    return render_template(
        'remove-tutorship.html',
        tutorship=tutorship
    )

