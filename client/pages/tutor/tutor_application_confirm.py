import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/tutor/application/confirm', methods=['POST'])
def tutor_application_confirm():
    # verify is student
    user = get_user(requests)
    print(user)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()



    course_id = request.form.get('course_id')
    print("hi")
    print(course_id)
    taken_course = request.form.get('taken_course')
    print(taken_course)
    experience = request.form.get('experience')
    print(experience)

   
    data = {
        'tutor_id': user['id'],
        'course_id': course_id,
        'taken_course': taken_course,
        'experience': experience,
        'status': 'REQUESTED'
    }

    # mark student as a tutor
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps({'id': str(user['id']), 'is_tutor': True}), headers=headers)
    if res.status_code != 200:
        return render_template(
            '/tutor/tutor-confirmation.html',
            message='Error: '  + str(res.content)
        )

    # create relationship btwn tutor and course
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/create/'), data=json.dumps(data), headers=headers)
    message = str(res)
    if res.status_code != 200:
        return render_template(
            '/tutor/tutor-confirmation.html',
            message='Error: ' + str(res.content)
        )


    return render_template(
        '/tutor/tutor-confirmation.html',
        message=message, 
        user=user
    )