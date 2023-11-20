import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template
from pages.shared.get_user import *


load_dotenv()

@app.route('/tutor/edit-profile')
def editBio():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': user['id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor = res.json()

    # get tutor_courses (deep)
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/deep/'), params={'tutor_id': user['id']}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutor_courses = res.json()
    tutor_courses.sort(key=lambda x: x["course"]["dept_course"])


    return render_template(
        '/tutor/tutor-edit-profile.html', tutor=tutor, user=user, tutor_courses=tutor_courses,
    )
