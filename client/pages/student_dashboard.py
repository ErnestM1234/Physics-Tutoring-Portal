
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template

load_dotenv()

@app.route('/student/dashboard')
def student_dashboard():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is student
    if "id" not in user.keys() or user['is_student'] == False:
        return redirect('/')

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': userId})
    tutorships = res.json()

    for tutorship in tutorships:
        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': tutorship['tutor_id']})
        tutor = res.json()
        tutorship['tutor'] = tutor

        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': tutorship['course_id']})
        course = res.json()
        tutorship['course'] = course

    return render_template(
        'student-dashboard.html',
        user=user,
        tutorships=tutorships
    )
