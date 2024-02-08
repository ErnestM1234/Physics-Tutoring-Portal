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
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()
    # get params
    course_id = request.form.get('course_id')
    taken_course = request.form.get('taken_course')
    experience = request.form.get('experience')


    # no need to do this cuz user must already be marked as tutor to access this page
    # # mark student as a tutor
    # res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps({'id': str(user['id']), 'is_tutor': True}), headers=headers)
    # if res.status_code != 200:
    #     session['error_message'] = str(res.content)
    #     return redirect('/error/')


    # check if a tutor course already exists
    tutor_course_id = None
    try:
        params = {
            'tutor_id': user['id'],
            'course_id': course_id,
        }
        res = requests.get(url=str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params=params, headers=headers)
        if res.status_code == 200:
            tutor_courses = res.json()
            if len(tutor_courses) > 0:
                tutor_course_id = int(tutor_courses[0]['id'])
    except:
        session['error_message'] = "An error has occured."
        return redirect('/error/')

    # create relationship btwn tutor and course
    # tutor_courses does exist
    if tutor_course_id != None:
        data = {
            'id': tutor_course_id,
            'tutor_id': user['id'],
            'course_id': course_id,
            'taken_course': taken_course,
            'experience': experience,
            'status': 'REQUESTED'
        }
        res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/update/'), data=json.dumps(data), headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
    # tutor_courses does not exist
    else:
        data = {
            'tutor_id': user['id'],
            'course_id': course_id,
            'taken_course': taken_course,
            'experience': experience,
            'status': 'REQUESTED'
        }
        res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/create/'), data=json.dumps(data), headers=headers)
        if res.status_code != 200:
            if res.content and isinstance(res.content, bytes):
                if res.content == b'{"message":"Cannot create duplicate tutor_courses."}\n':
                    session['error_message'] = "You have already applied to this coures."
                    return redirect('/error/')
                else:
                    session['error_message'] = "An error has occurred. Please check that the provided information is valid."
                    return redirect('/error/')
            session['error_message'] = str(res.content)
            return redirect('/error/')

    return redirect('/tutor/courses')