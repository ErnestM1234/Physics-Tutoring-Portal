import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/student/tutor/application/confirm', methods=['POST'])
def student_tutor_application_confirm():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_student'] == False:
        return render_template(
            '/student/student-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    #course_id = request.form.get('course_id')
    taken_course = request.form.get('taken_course')
    experience = request.form.get('experience')

   
    data = {
        'tutor_id': user['id'],
        'taken_course': taken_course,
        'experience': experience,
        'status': 'REQUESTED'
    }

    # mark student as a tutor
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps({'id': str(user['id']), 'is_tutor': True}), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    # create relationship btwn tutor and course
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/create/'), data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    message = str(res)

    return render_template(
        '/student/student-confirmation.html',
        message=message, 
        user=user
    )