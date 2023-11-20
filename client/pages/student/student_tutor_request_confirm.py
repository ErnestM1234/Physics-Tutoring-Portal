
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/tutor/request/confirm')
def student_tutor_request_confirm():

     # TO CHANGE
    course_id = request.args.get('course_id')
    tutor_id = request.args.get('tutor_id')

    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            '/student/student-no-access.html',
            message='you do not have permission to access this page'
        )
    
    # get headers
    headers = get_header()

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps({'tutor_id': tutor_id, 'course_id': course_id, 'student_id': user['id'], 'status': 'REQUESTED'}), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    return redirect('/student/dashboard')



@app.route('/student/tutor/request-all/confirm')
def student_tutor_request_all_confirm():

    # TO CHANGE
    course_id = request.args.get('course_id')

    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            '/student/student-no-access.html',
            message='you do not have permission to access this page'
        )
    
    # get headers
    headers = get_header()

    # request all tutors for given course
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/request-all/'), data=json.dumps({'course_id': course_id, 'student_id': user['id'], 'status': 'REQUESTED'}), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    return redirect('/student/dashboard')