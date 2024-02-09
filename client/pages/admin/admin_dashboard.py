
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
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()
    courses = []
    total_students = -1
    total_tutors = -1
    total_courses = -1

    # get stats
    try:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/dashboard_stats/'), params={}, headers=headers)
        if res.status_code != 200:
            print("Stats request raised exception: " + str(res.content))
            total_courses = -1
            total_students = -1
            total_tutors = -1
            courses = []
        else:
            stats = res.json()
            total_courses = stats["course_count"]
            total_students = stats["student_count"]
            total_tutors = stats["tutor_approved_count"]
            courses = stats["courses"]
    except Exception as e:
        print("Stats request raised exception: " + str(e))
    
    


    return render_template(
        '/admin/admin-dashboard.html',
        user=user,
        courses=courses,
        total_students=total_students,
        total_tutors=total_tutors,
        total_courses=total_courses
    )
