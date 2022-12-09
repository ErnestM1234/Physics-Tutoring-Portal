
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/dashboard')
def admin_dashboard():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    # get courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'), headers=headers)
    courses = res.json()

    # get tutors by coures
    # get tutees by course
    # todo(Ernest): spin up a diff process for these requests?? these two is a bit ~C~ ~H~ ~U~ ~N~ ~K~ ~Y~
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutor_courses/'), params={'status': "ACCEPTED"}, headers=headers)
    tutor_courses = res.json()
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'status': "ACCEPTED"}, headers=headers)
    tutorships = res.json()

    approved_tutors_count = []
    available_tutors_count = []
    tutees_count = []
    for course in courses: # todo (Ernest): this runs in like O(N^2) time. It can run in O(N) time. ATM I am too lazy to optimize this
        filtered_tutors = tutor_courses

        # calculate approved tutors
        approved_tutors_count.append(len(list(filter(lambda tutor_course: tutor_course['course_id'] == course['id'], tutor_courses))))

        # calculate available tutors
        available_tutors_count.append(3) # todo (Ernest): requires updates to the schema

        # calculate active tutees
        tutees_count.append(len(list(filter(lambda tutorship: tutorship['course_id'] == course['id'], tutorships))))




    return render_template(
        '/admin/admin-dashboard.html',
        user=user,
        courses=courses,
        approved_tutors_count=approved_tutors_count,
        available_tutors_count=available_tutors_count,
        tutees_count=tutees_count
    )
