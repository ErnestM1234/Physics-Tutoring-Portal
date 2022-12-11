import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/tutor/application')
def tutorApplication():
    # verify is student
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    course_id = request.args.get('course_id')
    print(course_id)
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
    course = res.json()



    # do we need these ? 
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'), headers=headers)
    courses = res.json()

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': user['id']}, headers=headers)
    tutor = res.json()

    return render_template(
        '/tutor/tutor-application.html', tutor=tutor, course = course

    )