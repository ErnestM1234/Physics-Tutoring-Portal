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


    course_id = request.form.get('course_id')
    taken_course = request.form.get('taken_course')
    experience = request.form.get('experience')
    puid = request.form.get('puid')

   
    data = {
        'tutor_id': user['id'],
        'course_id': course_id,
        'taken_course': taken_course,
        'experience': experience,
        'status': 'REQUESTED'
    }

    # make sure puid is an int
    MAX_PUID_NUM = 1000000000
    if puid is None or not puid.isdigit() or int(puid) > MAX_PUID_NUM:
        session['error_message'] = 'invalid puid'
        return redirect('/error/')

    # mark student as a tutor
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps({'id': str(user['id']), 'is_tutor': True, 'puid': puid}), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    # create relationship btwn tutor and course
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/create/'), data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        if res.content and isinstance(res.content, bytes):
            if res.content == b'{"message":"Cannot create duplicate tutor_courses."}\n':
                session['error_message'] = "You have already applied to this coures."
                return redirect('/error/')
            else:
                print(str(res.content))
                session['error_message'] = "An error has occurred. Please check that the provided information is valid."
                return redirect('/error/')

        session['error_message'] = str(res.content)
        return redirect('/error/')

    return redirect('/student/dashboard')