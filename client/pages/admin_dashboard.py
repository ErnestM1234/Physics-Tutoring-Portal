
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template

load_dotenv()

@app.route('/admin/dashboard')
def admin_dashboard():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if "id" not in user.keys() or user['is_admin'] == False:
        return redirect('/')

    # get courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))
    courses = res.json()

    # get tutors by coures
    # get tutees by course
    for course in courses:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_course/count/'), params={'course_id': course['id'],'status': "ACCEPTED"})
        if res.status_code != 200:
            message = str(res)
            return render_template(
                'confirmation.html',
                message=message
            )
        course['approved_tutor_count'] = res.json()

        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorship/count/'), params={'course_id': course['id']})
        if res.status_code != 200:
            message = str(res)
            return render_template(
                'confirmation.html',
                message=message
            )
        course['tutee_count'] = res.json()

    return render_template(
        'admin-dashboard.html',
        user=user,
        courses=courses,
    )
